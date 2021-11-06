// To execute Scala code, please define an object named Solution that extends App

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

object Job {
 
  def main(args: Array[String]): Unit = {
    val spark: SparkSession = SparkSession.builder()
    .appName("testing")
    .enaleHiveSupport()
    .getOrCreate()
    
    val addUdf = udf((p1: Integer, p2: Integer) => p1 + p2)
    
    val dfEmployees = spark.read.parquet("gcs://foo/employee/data")
      .select(col("name").as("employee_name"), col("title"))
      .as("employees")
      .cache()
    val dfFilteredIncidents = spark.read.parquet("gcs://foo/records/data")
      .dropDuplicates()
      .where(col("rank") > 3 and col("is_incident") === true)
      .withColumn("adjusted_rank", addUdf(col("rank"), lit(1)))
      .as("incidents")
      .cache()
    
    val empsWithRecordsDf = dfEmployees
      .join(dfFilteredIncidents, col("incidents.employee_id") == col("employees.id"))
    
    val sumRecordsDf = 
      empsWithRecordsDf
        .groupBy("id")
        .agg(
          count(*).as("num_incidents")
        )
        .orderBy("num_incidents")
    
    sumRecordsDf.createOrReplaceTempView("incidents_per_employee")
    sumRecordsDf.show(10) //top 10
    sumRecordsDf.save("incidents_per_employee.parquet")
  }
}
