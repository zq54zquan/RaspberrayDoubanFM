#!doubanFMLogin.py
import urllib
import urllib2
import json
import vlc
import subprocess
import thread
DOUBANDOMAIN = "http://www.douban.com/"
LOGINPATH = "j/app/login"
CHANNELPATH = "j/app/radio/channels"
SONGSPATH = "j/app/radio/people"

class Channel:
	"""Channel"""
	def __init__(self, name, seq_id,abbr_en,channel_id,name_en):
		self.name = name
		self.seq_id = seq_id;
		self.abbr_en = abbr_en;
		self.channel_id = channel_id;
		self.name_en = name_en;

class Song:
	"""Song Modle in Radio"""
	def __init__(self, picture,album,ssid,artist,url,company,title,rating_avg,length,subtype,public_time,sid,aid,sha256,kbps,albumtitle,like):
		
		self.picture = picture
		self.album = album
		self.ssid = ssid;
		self.artist = artist
		self.url = url
		self.company = company
		self.title = title;
		self.rating_avg = rating_avg
		self.length = length
		self.subtype = subtype
		self.public_time = public_time;
		self.sid = sid;
		self.aid = aid;
		self.sha256 = sha256
		self.kbps = kbps
		self.albumtitle = albumtitle;
		self.like = like;
		

class Doubaner:
	"""Doubaner"""
	def __init__(self, user_id,token,expire,user_name,email):
		self.user_id = user_id;
		self.token = token;
		self.expire = expire;
		self.user_name = user_name;
		self.email = email;
		
		

class DouBanFMOnBerray:
	"""DouBanFMOnBerray prepare for raspberry, let it play douban fm
	TODO: Download the favorite music
	"""
	def __init__(self):
		self.channels = [];
		self.channelSongs = {}
		self.player = None
		self.currentSongs = []
		self.index = 0
		self.user = None;
	def login(self,uname,passwd):
		data = urllib.urlencode({"email":uname,"password":passwd,"app_name":"radio_desktop_win","version":"100"});
		req = urllib2.Request(DOUBANDOMAIN+LOGINPATH,data);

		req_data = urllib2.urlopen(req);
		res = req_data.read();
		result = json.loads(res);
		doubaner = Doubaner(result["user_id"], result["token"], result["expire"], result["user_name"], result["email"]);
		return doubaner;
	def getChannels(self):
		req = urllib2.Request(DOUBANDOMAIN+CHANNELPATH);

		req_data = urllib2.urlopen(req);
		res = req_data.read();
		result = json.loads(res);
		channelDics = result["channels"];
		for channelDic in channelDics:
			picChannel = Channel(channelDic["name"].encode("utf-8"), channelDic["seq_id"], channelDic["abbr_en"].encode("utf-8"), channelDic["channel_id"], channelDic["name_en"].encode("utf-8"))
			self.channels.append(picChannel);

	def getSongs(self,user_id,expire,token,channel_id):
		queryStr = "?"
		if user_id:
			queryStr+="user_id="+user_id
		if expire:
			if len(queryStr)!=1:
				queryStr+="&expire="+expire;
			else:
				queryStr+="expire="+expire;
		if token:
			if len(queryStr)!=1:
				queryStr+="&token="+token
			else:
				queryStr+="token="+token
		if channel_id:
			if len(queryStr)!=1:
				queryStr+="&channel="+channel_id;
			else:
				queryStr+="channel="+channel_id;
		if len(queryStr)!=1:
			queryStr+="&type=n"
		else:
			queryStr += "type=n"
		if len(queryStr)!=1:
			queryStr+="&version="+"100"
		else:
			queryStr+="version="+"100"

		if len(queryStr)!=1:
			queryStr+="&app_name="+"radio_desktop_win"
		else:
			queryStr+="app_name="+"radio_desktop_win"
		req = urllib2.Request(DOUBANDOMAIN+SONGSPATH+queryStr);
		req_data = urllib2.urlopen(req);
		res = req_data.read();			
		result = json.loads(res);
		songDics = result["song"];
		songarrray = [];

		for songDic in songDics:
			if songDic["sid"].isdigit():
				song = Song(songDic["picture"].encode("utf-8"), songDic["album"].encode("utf-8"), songDic["ssid"].encode("utf-8"), songDic["artist"].encode("utf-8"), songDic["url"].encode("utf-8"), songDic["company"].encode("utf-8"), songDic["title"].encode("utf-8"), songDic["rating_avg"], songDic["length"], songDic["subtype"].encode("utf-8"), songDic["public_time"].encode("utf-8"), songDic["ssid"].encode("utf-8"), songDic["aid"].encode("utf-8"), songDic["sha256"].encode("utf-8"), songDic["kbps"].encode("utf-8"), songDic["albumtitle"].encode("utf-8"), songDic["like"])
				songarrray.append(song)
		self.channelSongs[channel_id]=songarrray;
		return self.channelSongs[channel_id] 

	def play(self):
		"""intall mpg123:brew install mpg123"""
		song = self.currentSongs[self.index]
		filename = song.url;
		print(song.title)
		self.stop()
		if self.player == None:
			self.player = subprocess.Popen(["mpg123",filename]);
			self.player.wait()
			self.player = None
			self.playnext()

	def stop(self):
		if self.player != None:
			self.player.kill()
			self.player = None;

	def playnext(self):
		self.index+=1
		print(self.index);
		if self.index == len(self.currentSongs):
			songs = self.getSongs(self.user.user_id, self.user.expire, self.user.token, str(self.channels[0].channel_id));
			self.currentSongs = songs;
			self.index = 0;
			print("next bounce songs");
		self.index = self.index%len(self.currentSongs)
		if self.player!=None:
			self.stop()
		self.play()

	def playMusicFormFM(self,uname,passwd):	
		self.user = self.login(uname,passwd);
		print(self.user.token)
		self.getChannels();

		songs = self.getSongs(self.user.user_id, self.user.expire, self.user.token, str(self.channels[0].channel_id));
		self.currentSongs = songs;
		self.index = -1;
		self.playnext()




