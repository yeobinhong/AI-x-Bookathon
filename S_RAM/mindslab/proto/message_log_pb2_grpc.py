# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from proto import message_log_pb2 as proto_dot_message__log__pb2


class MessageLoggerStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.LogMessage = channel.unary_unary(
        '/maum.brain.MessageLogger/LogMessage',
        request_serializer=proto_dot_message__log__pb2.LogRequest.SerializeToString,
        response_deserializer=proto_dot_message__log__pb2.LogResponse.FromString,
        )


class MessageLoggerServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def LogMessage(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_MessageLoggerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'LogMessage': grpc.unary_unary_rpc_method_handler(
          servicer.LogMessage,
          request_deserializer=proto_dot_message__log__pb2.LogRequest.FromString,
          response_serializer=proto_dot_message__log__pb2.LogResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'maum.brain.MessageLogger', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))