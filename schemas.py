from marshmallow import Schema, fields


class PLainItemSchema(Schema):
    id = fields.Str(dump_only = True)
    name = fields.Str(required = True)
    price = fields.Float(required = True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

class PLainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class ItemSchema(PLainItemSchema):
    store_id = fields.Int(load_only=True)
    store= fields.Nested(PLainStoreSchema(), dump_only = True) ## For output onlyn -- It automatically includes the Store object associated with the Item when you serialize it.
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class TagUpdateSchema(Schema):
    name = fields.Str()

class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PLainStoreSchema(),
                          dump_only=True)  ## For output onlyn -- It automatically includes the Store object associated with the Item when you serialize it.
    items = fields.List(fields.Nested(PLainItemSchema()), dump_only=True)

class StoreSchema(PLainStoreSchema):
    items = fields.List(fields.Nested(PLainItemSchema(), dump_only=True))
    tags = fields.List(fields.Nested(PlainTagSchema(), dump_only=True))

class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)

class UserSchema(Schema):
    id = fields.Int(dump_only= True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True) ##   load_only=True to not send the password back or make it move around the network
