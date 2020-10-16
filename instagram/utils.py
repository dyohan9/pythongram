import hashlib
import hmac
import urllib.parse
import uuid

from instagram import config


class Utils:
    @staticmethod
    def generateUUID(uuid_type):
        generated_uuid = str(uuid.uuid4())
        if uuid_type:
            return generated_uuid
        else:
            return generated_uuid.replace("-", "")

    @staticmethod
    def generateDeviceId(seed):
        volatile_seed = "12345"
        m = hashlib.md5()
        m.update(seed.encode("utf-8") + volatile_seed.encode("utf-8"))
        return "android-" + m.hexdigest()[:16]

    @staticmethod
    def generateSignature(data):
        try:
            parsedData = urllib.parse.quote(data)
        except AttributeError:
            parsedData = urllib.quote(data)

        return (
            "ig_sig_key_version="
            + config.SIG_KEY_VERSION
            + "&signed_body="
            + hmac.new(
                config.IG_SIG_KEY.encode("utf-8"), data.encode("utf-8"), hashlib.sha256
            ).hexdigest()
            + "."
            + parsedData
        )
