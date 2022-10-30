#
# Autogenerated by Thrift Compiler (0.16.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec

import sys

from thrift.transport import TTransport
all_structs = []


class Player(object):
    """
    Attributes:
     - id
     - username
     - photo
     - rating
     - channel_name
     - operate
     - bot_id
     - game_id

    """


    def __init__(self, id=None, username=None, photo=None, rating=None, channel_name=None, operate=None, bot_id=None, game_id=None,):
        self.id = id
        self.username = username
        self.photo = photo
        self.rating = rating
        self.channel_name = channel_name
        self.operate = operate
        self.bot_id = bot_id
        self.game_id = game_id

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.I32:
                    self.id = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.username = iprot.readString().decode('utf-8', errors='replace') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.photo = iprot.readString().decode('utf-8', errors='replace') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.I32:
                    self.rating = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.STRING:
                    self.channel_name = iprot.readString().decode('utf-8', errors='replace') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 6:
                if ftype == TType.I32:
                    self.operate = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 7:
                if ftype == TType.I32:
                    self.bot_id = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 8:
                if ftype == TType.I32:
                    self.game_id = iprot.readI32()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('Player')
        if self.id is not None:
            oprot.writeFieldBegin('id', TType.I32, 1)
            oprot.writeI32(self.id)
            oprot.writeFieldEnd()
        if self.username is not None:
            oprot.writeFieldBegin('username', TType.STRING, 2)
            oprot.writeString(self.username.encode('utf-8') if sys.version_info[0] == 2 else self.username)
            oprot.writeFieldEnd()
        if self.photo is not None:
            oprot.writeFieldBegin('photo', TType.STRING, 3)
            oprot.writeString(self.photo.encode('utf-8') if sys.version_info[0] == 2 else self.photo)
            oprot.writeFieldEnd()
        if self.rating is not None:
            oprot.writeFieldBegin('rating', TType.I32, 4)
            oprot.writeI32(self.rating)
            oprot.writeFieldEnd()
        if self.channel_name is not None:
            oprot.writeFieldBegin('channel_name', TType.STRING, 5)
            oprot.writeString(self.channel_name.encode('utf-8') if sys.version_info[0] == 2 else self.channel_name)
            oprot.writeFieldEnd()
        if self.operate is not None:
            oprot.writeFieldBegin('operate', TType.I32, 6)
            oprot.writeI32(self.operate)
            oprot.writeFieldEnd()
        if self.bot_id is not None:
            oprot.writeFieldBegin('bot_id', TType.I32, 7)
            oprot.writeI32(self.bot_id)
            oprot.writeFieldEnd()
        if self.game_id is not None:
            oprot.writeFieldBegin('game_id', TType.I32, 8)
            oprot.writeI32(self.game_id)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(Player)
Player.thrift_spec = (
    None,  # 0
    (1, TType.I32, 'id', None, None, ),  # 1
    (2, TType.STRING, 'username', 'UTF8', None, ),  # 2
    (3, TType.STRING, 'photo', 'UTF8', None, ),  # 3
    (4, TType.I32, 'rating', None, None, ),  # 4
    (5, TType.STRING, 'channel_name', 'UTF8', None, ),  # 5
    (6, TType.I32, 'operate', None, None, ),  # 6
    (7, TType.I32, 'bot_id', None, None, ),  # 7
    (8, TType.I32, 'game_id', None, None, ),  # 8
)
fix_spec(all_structs)
del all_structs
