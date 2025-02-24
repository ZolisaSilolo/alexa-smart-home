from flask import jsonify
import boto3
import json

class DeviceController:
    def __init__(self, iot_client=None):
        if iot_client is None:
            self.iot_client = boto3.client('iot-data', region_name='us-east-1')  # Replace 'region' with your AWS region
        else:
            self.iot_client = iot_client

    def turn_on_device(self, device_id):
        payload = json.dumps({"state": {"desired": {"power": "ON"}}})
        response = self.iot_client.update_thing_shadow(
            thingName=device_id,
            payload=payload
        )
        return jsonify({"status": "success", "message": f"Device {device_id} turned on."})

    def turn_off_device(self, device_id):
        payload = json.dumps({"state": {"desired": {"power": "OFF"}}})
        response = self.iot_client.update_thing_shadow(
            thingName=device_id,
            payload=payload
        )
        return jsonify({"status": "success", "message": f"Device {device_id} turned off."})

    def adjust_device_setting(self, device_id, setting, value):
        payload = json.dumps({"state": {"desired": {setting: value}}})
        response = self.iot_client.update_thing_shadow(
            thingName=device_id,
            payload=payload
        )
        return jsonify({"status": "success", "message": f"Device {device_id} setting {setting} adjusted to {value}."})