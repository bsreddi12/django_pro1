class EC2:
    def __init__(self, client):
        self._client = client
        """ :type : pyboto3.ec2 """
    def create_key_pair(self, key_name):
        print()
        return self._client.create_key_pair(
            KeyName=key_name,
        )

    def create_security_group(self):
        return self._client.create_security_group(

        )