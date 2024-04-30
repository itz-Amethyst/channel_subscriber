from core.errors.main import CustomErrorSerializer

bad_verification = CustomErrorSerializer(4002, 'Bad Verification', 'Invalid Verification', 400)
no_change = CustomErrorSerializer(4003, 'No Change', 'Nothing to Change', 400)
bad_id = CustomErrorSerializer(4004, 'Bad ID', 'Invalid ID', 404, extra={'id': 21})
bad_auth = CustomErrorSerializer(4005, 'Invalid Authentication Credentials', 'Invalid authentication credentials', 403)
forbidden = CustomErrorSerializer(4006, 'Forbidden', 'Not Enough Permissions', 403)
rate_limited = CustomErrorSerializer(4007, 'Rate Limited', 'Too Many Requests', 429)
bad_args = CustomErrorSerializer(4009, 'Bad Args', 'Invalid args', 400)
bad_file = CustomErrorSerializer(40013, 'Bad File', 'Invalid or unknown file', 400)
not_unique = CustomErrorSerializer(4014, 'Not Unique', '{} is not unique', 400, extra={'value': 'xxx'})
same_role = CustomErrorSerializer(40009, 'Same Role', 'User is in the same role', 409)


all_client_errors = {
    bad_verification, bad_id, no_change, bad_auth,
    forbidden, rate_limited, bad_args, bad_file,
    not_unique, same_role
}