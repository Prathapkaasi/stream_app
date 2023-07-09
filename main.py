from database import DB
import streamlit as stl

chosen_option = stl.text_input("Enter Valid Id")
stl.button("Get Channel Stats")
c_id = "UCUAaV8D54bHDfSNLhWS61Ow"
channel_info = DB().query_data("select * from channel_info where channel_id ='{}'".format(chosen_option))
videos = DB().query_data("select * from videos where channel_id = '{}'".format(chosen_option))
print(len(videos))


def get_data():
    stl.header("Channel Info")
    stl.json(channel_info)
    stl.header("Playlist Id Videos")
    stl.json(videos)


if len(chosen_option) <= 0:
    stl.header("Search With valid Id")
elif len(channel_info) <= 0:
    stl.header("No Channel found")
else:
    get_data()
