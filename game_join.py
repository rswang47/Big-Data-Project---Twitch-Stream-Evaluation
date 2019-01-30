
from pyspark.sql import SparkSession, functions, types
import sys
import json

def join():
	stream_df = spark.read.json('stream_cleanned')
	giant_df = spark.read.json('game_info_base')

	stream_df = stream_df.withColumn('gen_name', functions.lower(stream_df.game))
	stream_df = stream_df.select('stream_id', 'gen_name').distinct()
	game_info = stream_df.groupBy('gen_name').count().cache()

	real_game_info = game_info.join(giant_df, game_info.gen_name == functions.lower(giant_df.name), 'left')

	real_game_info = real_game_info.orderBy(real_game_info.count.desc())

	real_game_info.where(real_game_info.count < 100).count().show()

	real_game_info.coalesce(1).write.json('real_game_info', mode = 'overwrite')

def read_guid():
	guids = spark.read.json('guids', multiLine=True).repartition(10)
	guids = guids.select('results.guid', 'results.genres')
	guids = guids.select('guid', functions.explode('genres').alias('genres'))
	guids = guids.select('guid', 'genres.name')
	guids = guids.groupBy('guid').agg(functions.collect_set('name'))
	guids.coalesce(1).write.json('game_genre', mode = 'overwrite')
  
if __name__ == '__main__':
	spark = SparkSession.builder.appName('join data').getOrCreate()
	spark.sparkContext.setLogLevel('WARN')
	read_guid()