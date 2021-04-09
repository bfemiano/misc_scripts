defmodule LongestRunning do
    def check(val, state) do
        case state.cur_val do
            nil ->
                %{cur_val: val, cur_cnt: 1, max_cnt: 1, max_val: val}
            ^val ->
                cur_cnt = state.cur_cnt + 1
                case cur_cnt > state.max_cnt do
                    true ->
                        %{cur_val: val, cur_cnt: cur_cnt, max_val: val, max_cnt: cur_cnt}
                    _ ->
                        %{state | cur_val: val, cur_cnt: cur_cnt}
                end
            _ -> %{state | cur_val: val, cur_cnt: 1}
        end
    end
end

defmodule Tests do
    use ExUnit.Case

    test "finds longest streak even when other characters appear more" do
        data = ["a", "b", "b", "b", "a", "a", "c", "a"]
        state = %{cur_val: nil, cur_cnt: 0, max_val: nil, max_cnt: 0}
        final_state = Enum.reduce(data, state, fn val, state -> LongestRunning.check(val, state) end)
        assert final_state.max_val == "b"
        assert final_state.max_cnt == 3
    end

    test "finds streak at end" do
        data = ["a", "b", "b", "b", "a", "a", "c", "a", "a", "a", "a"]
        state = %{cur_val: nil, cur_cnt: 0, max_val: nil, max_cnt: 0}
        final_state = Enum.reduce(data, state, fn val, state -> LongestRunning.check(val, state) end)
        assert final_state.max_val == "a"
        assert final_state.max_cnt == 4
    end

    test "finds streak at beginning" do
        data = ["b", "b", "b", "a", "a", "c", "a", "a"]
        state = %{cur_val: nil, cur_cnt: 0, max_val: nil, max_cnt: 0}
        final_state = Enum.reduce(data, state, fn val, state -> LongestRunning.check(val, state) end)
        assert final_state.max_val == "b"
        assert final_state.max_cnt == 3
    end

    test "finds single item as longest streak" do
        data = ["b"]
        state = %{cur_val: nil, cur_cnt: 0, max_val: nil, max_cnt: 0}
        final_state = Enum.reduce(data, state, fn val, state -> LongestRunning.check(val, state) end)
        assert final_state.max_val == "b"
        assert final_state.max_cnt == 1
    end

    test "handles empty" do
        data = []
        state = %{cur_val: nil, cur_cnt: 0, max_val: nil, max_cnt: 0}
        final_state = Enum.reduce(data, state, fn val, state -> LongestRunning.check(val, state) end)
        assert final_state.max_val == nil
        assert final_state.max_cnt == 0
    end
end
