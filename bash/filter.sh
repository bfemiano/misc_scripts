#!/bin/bash
if [ $# -lt 3 ] ; then
 echo "Usage: ./filter.sh table_name column value"
 exit 1
fi
echo "scan '$1', {FILTER=>org.apache.hadoop.hbase.filter.SingleColumnValueFilter.new(org.apache.hadoop.hbase.util.Bytes.toBytes('taint'),org.apache.hadoop.hbase.util.Bytes.toBytes('$2'),org.apache.hadoop.hbase.filter.CompareFilter::CompareOp.valueOf('EQUAL'),org.apache.hadoop.hbase.util.Bytes.toBytes('$3'))}" | hbase shell
