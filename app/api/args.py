from marshmallow import Schema, fields, missing, validate, ValidationError
import json

from numpy import require


class MyObjectField(fields.Field):
    default_error_messages = {
        'invalid': 'Please provide a valid json string.',
    }

    # 反序列化生成对象
    def _deserialize(self, value, attr, obj, **kwargs):
        if not value:
            raise ValidationError(u'空值不能转化')
        try:
            return json.loads(value)
        except ValueError:
            raise ValidationError(u'json字符串格式错误')

    # 序列化对象输出
    def _serialize(self, value, attr, data, **kwargs):
        return json.dumps(value)


class QrEncodeArgs(Schema):
    text = fields.String(required=True, validate=validate.Length(min=1))

    class Meta:
        strict = True


class JwtDecodeArgs(Schema):
    encode = fields.String(required=True, validate=validate.Length(min=1))

    class Meta:
        strict = True


def validate_dict(data):
    if not data:
        raise ValidationError("字段不能为空")


class HashSaltArgs(Schema):
    # 加密操作/解密操作
    encrypt = fields.Boolean(missing=True)
    salt = fields.String(missing="")
    skips = fields.List(fields.String(
        allow_none=False, validate=validate.Length(min=1)), missing=[])
    data = fields.List(fields.Dict(keys=fields.Str(), required=True, values=fields.Str(),
                                   validate=validate_dict, allow_none=False), validate=validate.Length(min=1))

    class Meta:
        strict = True


class CurlArgs(Schema):
    url = fields.String(required=True, validate=validate.Length(min=1))
    methods = fields.String(
        required=True, validate=validate.OneOf(["GET", "POST", "DELETE"]))
    params = MyObjectField()
    cookies = fields.Dict(keys=fields.Str(), values=fields.Str())
    headers = fields.Dict(keys=fields.Str(), values=fields.Str())
    bodyType = fields.String(
        required=True, validate=validate.OneOf(['text', 'json', 'binary']))
    textBody = fields.String(validate=validate.Length(min=1))

    class Meta:
        strict = True
