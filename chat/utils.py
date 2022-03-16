from django.core.serializers.python import Serializer

class RoomMessagesSerializer(Serializer):
    def get_dump_object(self,obj):
        dump_object={}
        dump_object.update({'username':str(obj.sender)})
        dump_object.update({'message':str(obj.message)})
        dump_object.update({'message_id':str(obj.id)})
        return dump_object