from infi.clickhouse_orm import Model, UInt8Field, Float32Field, DateTimeField, Buffer, MergeTree, BufferModel


class CPUStat(Model):
    cpu_id = UInt8Field()
    cpu_percent = Float32Field()
    timestamp = DateTimeField()

    engine = MergeTree(order_by=[cpu_id], date_col='timestamp')


class CPUStatBuffer(BufferModel, CPUStat):
    engine = Buffer(CPUStat)