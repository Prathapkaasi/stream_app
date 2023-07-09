import mysql.connector

from youtube import YoutubeFinder



class DB:
    def __init__(self):
        self.cursor = self.db_connect()

    def db_connect(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='prathapkasi',
                database='streamapp'
            )
            self.connection = connection
            cursor = connection.cursor()
            return cursor

        except mysql.connector.errors as error:
            print("Error connecting DB!", error)

        finally:
            if connection.is_connected():
                print("DB! connected")

    def query_data(self, query):
        self.cursor.execute(query)

        rows = self.cursor.fetchall()
        columns_name = self.cursor.column_names
        # print(columns_name)
        result = []
        for row in rows:
            row_dict = dict(zip(columns_name, row))
            result.append(row_dict)

        return result

    def insert_data(self):
        ytube = YoutubeFinder()
        # inserting channel info
        channel_info = ytube.get_channel_info("snippet,contentDetails,statistics", "")

        # columns = ', '.join(channel_info.keys())
        # placeholders = ', '.join(['%s'] * len(columns.split(",")))
        # insert_query = "INSERT INTO channel_info({}) VALUES({})".format(columns, placeholders)
        # values = tuple(channel_info.values())
        # print(insert_query)
        # self.cursor.execute(insert_query, values)
        # if self.cursor.rowcount > 0:
        #     print("Inserted! Row Affected")

        # Playlist inserting
        playlists = ytube.get_playlist("contentDetails", ytube.play_list_id)

        video_list_col = []
        video_lists = []
        video_len = 0
        for x in ytube.video_ids:
            video = ytube.get_video_info("snippet,statistics", x)
            video_len += 1
            video_lists.append(video)
            if video_len == 1:
                video_list_col.append((video))
        video_columns = ", ".join(video_list_col[0].keys())

        videos_placeholders = ', '.join(['%s'] * len(video_columns.split(",")))
        video_query = "INSERT IGNORE  INTO videos({}) VALUES({})".format(video_columns, videos_placeholders)

        for video in video_lists:
            self.cursor.execute(video_query, tuple(video.values()))
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
