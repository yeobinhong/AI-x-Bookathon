# NSG Engine Controller for AI x bookathon.
# MindsLab, Inc.
# 
# It works as a client, sending requests to a engine-control server on the other container.
# This code holds basic structure but perhaps insufficient.
# You may adjust below as much as you wish for your efficiency.

import argparse
import grpc
from proto.engine_control_pb2 import ControlRequest
from proto.engine_control_pb2 import IDLE, TRAINING, INFERRING, INVALID_REQUEST
from proto.engine_control_pb2 import CHECK_STATUS, START_TRAINING, START_INFERRING, STOP_OPERATION
from proto.engine_control_pb2_grpc import EngineControllerStub
from proto.message_log_pb2 import LogRequest
from proto.message_log_pb2 import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
from proto.message_log_pb2_grpc import MessageLoggerStub

# Do not change these lines. Connections will be lost.
# If you are to use another source code. Utilize LOG_END_POINT and implementation example below for logging.
GRPC_END_POINT = 'localhost:35000'   
LOG_END_POINT = 'localhost:36000'

instruction_str2enum = {
    'check_status': CHECK_STATUS,
    'start_training': START_TRAINING, 
    'start_inferring': START_INFERRING,
    'stop_operation': STOP_OPERATION
}
status_enum2str = {
    IDLE: 'idle',
    TRAINING: 'training',
    INFERRING: 'inferring',
    INVALID_REQUEST: 'invalid_request',
}

def request_control(request):
    with grpc.insecure_channel(GRPC_END_POINT) as channel:
        stub = EngineControllerStub(channel)
        response = stub.ControlEngine(request)

        return response

def process_control_response(response, instruction):
    status = response.status
    msg = response.msg
    infer_results = response.infer_results

    print('[Status] {}\n[Message] {}'.format(status_enum2str[status], msg))
    if instruction_str2enum[instruction] == START_INFERRING:
        for infer_result in infer_results:
            print(infer_result)

        # Logging
        msg = 'Prompt: {}\nGenerated: {}'.format(
                args.infer_text, 
                '\n'.join(['{}. {}'.format(idx+1, text) for idx, text in enumerate(response.infer_results)]))
        log_request = LogRequest(log_level=DEBUG, msg=msg)

        log_response = request_log(log_request)
        assert log_response.done is True

def request_log(request):
    with grpc.insecure_channel(LOG_END_POINT) as channel:
        stub = MessageLoggerStub(channel)
        response = stub.LogMessage(request)

        return response


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--instruction', type=str, required=True, 
            choices=['check_status', 'start_training', 'start_inferring', 'stop_operation'])
    parser.add_argument('--config_path', type=str, default='cfg/config.yml')
    parser.add_argument('--infer_text', type=str)

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = parse_args()

    request = ControlRequest(
            instruction = instruction_str2enum[args.instruction], 
            config_path = args.config_path, 
            infer_text  = args.infer_text)

    print('Requesting {}.. it may take a while to start training & inferring\n'.format(args.instruction))
    response = request_control(request)

    print('Received response:')
    process_control_response(response, args.instruction)
