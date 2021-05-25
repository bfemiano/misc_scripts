defmodule CircularBuffer do
  use GenServer
  require Logger

  defmodule State do
    defstruct [:read_pos, :write_pos, :size, :buffer]

    def read(%{read_pos: read_pos, write_pos: write_pos, size: size, buffer: buffer} = state) do
      read_pos =
        case read_pos do
          # if the read pointer has reached the end of the buffer, wrap around.
          ^size -> 0
          _ -> read_pos
        end

      {item, new_buffer, next_read_pos} =
        case read_pos do
          # if the read pointer = write pointer then we have an empty list.
          ^write_pos ->
            {nil, buffer, read_pos + 0}

          _ ->
            {:array.get(read_pos, buffer), buffer, read_pos + 1}
        end

      write_pos =
        case write_pos do
          # if the write pointer has reached the end of the buffer, wrap around.
          ^size -> 0
          _ -> write_pos
        end

      {item, %State{state | read_pos: next_read_pos, write_pos: write_pos, buffer: new_buffer}}
    end

    def write(item, %State{write_pos: write_pos, size: size, buffer: buffer} = state) do
      write_pos =
        case write_pos do
          # if the write pointer has reached the end of the buffer, wrap around.
          ^size -> 0
          _ -> write_pos
        end

      %State{state | write_pos: write_pos + 1, buffer: :array.set(write_pos, item, buffer)}
    end
  end

  # Easier to play around with if it's not linked to any other process.
  def start_link(size: size) when size > 0 do
    GenServer.start_link(__MODULE__, %State{
      read_pos: 0,
      write_pos: 0,
      size: size,
      buffer: :array.new(size)
    })
  end

  def start_link(size: _size), do: raise("Size of circular buffer must be > 0.")

  def write(pid, item) do
    GenServer.call(pid, {:write, item}, 60)
  end

  def read(pid) do
    GenServer.call(pid, :read, 60)
  end

  @impl true
  def init(state) do
    {:ok, state}
  end

  @impl true
  def handle_call(
        :read,
        _from,
        state
      ) do
    {item, state} = State.read(state)
    {:reply, item, state}
  end

  @impl true
  def handle_call(
        {:write, item},
        _from,
        state
      ) do
    {:reply, nil, State.write(item, state)}
  end
end

defmodule CircularBufferTest do
  use ExUnit.Case

  test "single item written to buffer can be read back." do
    {:ok, pid} = CircularBuffer.start_link(size: 1)
    CircularBuffer.write(pid, "hi")
    "hi" = CircularBuffer.read(pid)
  end

  test "multiple items written to buffer can be read back in FIFO order." do
    {:ok, pid} = CircularBuffer.start_link(size: 2)
    CircularBuffer.write(pid, "hi")
    CircularBuffer.write(pid, "there")
    "hi" = CircularBuffer.read(pid)
    "there" = CircularBuffer.read(pid)
  end

  test "buffer that exceeds size starts having contents overwritten." do
    {:ok, pid} = CircularBuffer.start_link(size: 3)
    CircularBuffer.write(pid, "foo1")
    CircularBuffer.write(pid, "foo2")
    CircularBuffer.write(pid, "foo3")
    CircularBuffer.write(pid, "foo4")

    "foo4" = CircularBuffer.read(pid)
  end

  test "empty buffer read returns nil." do
    {:ok, pid} = CircularBuffer.start_link(size: 1)
    nil = CircularBuffer.read(pid)
  end

  test "buffer cannot be created with size 0" do
    assert_raise(RuntimeError, "Size of circular buffer must be > 0.", fn ->
      CircularBuffer.start_link(size: -1)
    end)
  end

  test "reads pickup where leftoff even after writes come in later" do
    {:ok, pid} = CircularBuffer.start_link(size: 3)
    CircularBuffer.write(pid, "foo1")
    CircularBuffer.write(pid, "foo2")
    CircularBuffer.write(pid, "foo3")
    "foo1" = CircularBuffer.read(pid)
    "foo2" = CircularBuffer.read(pid)
    # overwrites pos 0
    CircularBuffer.write(pid, "foo4")
    "foo3" = CircularBuffer.read(pid)
    "foo4" = CircularBuffer.read(pid)
  end

  test "reads that catchup to all writes produce nil on next read." do
    {:ok, pid} = CircularBuffer.start_link(size: 3)
    CircularBuffer.write(pid, "foo1")
    CircularBuffer.write(pid, "foo2")
    CircularBuffer.write(pid, "foo3")

    "foo1" = CircularBuffer.read(pid)
    "foo2" = CircularBuffer.read(pid)
    "foo3" = CircularBuffer.read(pid)
    nil = CircularBuffer.read(pid)
  end

  test "multiple buffers can exist under different pids and work fine in the same application." do
    {:ok, foo_pid} = CircularBuffer.start_link(size: 1)
    {:ok, bar_pid} = CircularBuffer.start_link(size: 1)
    CircularBuffer.write(foo_pid, "foo")
    CircularBuffer.write(bar_pid, "bar")

    "foo" = CircularBuffer.read(foo_pid)
    "bar" = CircularBuffer.read(bar_pid)
  end
end
