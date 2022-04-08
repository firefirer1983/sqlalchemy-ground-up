#! /usr/bin/env python
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session

Base = declarative_base()

db = sa.create_engine(
    "mysql+pymysql://root:123456789@127.0.0.1:3306/xinda_gd?charset=utf8mb4", echo=True
)


class User(Base):
    __tablename__ = "tb_user"
    __table_args__ = ({"comment": "用户表"},)
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    create_time = sa.Column(sa.DateTime, default=datetime.now)
    update_time = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)
    username = sa.Column(sa.String(50), comment="用户名")


class Department(Base):
    __tablename__ = "tb_department"
    __table_args__ = ({"comment": "部门表"},)
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    create_time = sa.Column(sa.DateTime, default=datetime.now)
    update_time = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)


class WarehouseGoodsShelf(Base):
    __tablename__ = "tb_warehouse_goods_shelf"
    __table_args__ = ({"comment": "货架表"},)
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    create_time = sa.Column(sa.DateTime, default=datetime.now)
    update_time = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)


class QualityStandardManage(Base):
    __tablename__ = "tb_quality_standard_manage"
    __table_args__ = ({"comment": "质检规格档案表"},)
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    create_time = sa.Column(sa.DateTime, default=datetime.now)
    update_time = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)



class QualityStandardManage(Base):
    __tablename__ = "tb_braid_plan_schedule"
    __table_args__ = ({"comment": "生产单表"},)
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    create_time = sa.Column(sa.DateTime, default=datetime.now)
    update_time = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)


class Warehouse(Base):
    __tablename__ = "tb_warehouse"
    __table_args__ = ({"comment": "存库表"},)
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    create_time = sa.Column(sa.DateTime, default=datetime.now)
    update_time = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)


class MaterialRecord(Base):
    __tablename__ = "tb_material_record"
    __table_args__ = ({"comment": "库存档案表"},)
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    create_time = sa.Column(sa.DateTime, default=datetime.now)
    update_time = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)

    material_id = sa.Column(sa.String(50), comment="存货编号/物料编码")
    material_type = sa.Column(sa.Integer, comment="存货类型 物料/半成品/成品")
    super_class = sa.Column(sa.String(50), comment="存货大类编码")
    has_detail = sa.Column(sa.Boolean, comment="是否存在明细(是否使用标签)")


class RawMaterial(Base):
    __tablename__ = "tb_raw_material"
    __table_args__ = ({"comment": "原材料物料表"},)
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    create_time = sa.Column(sa.DateTime, default=datetime.now)
    update_time = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)

    number = sa.Column(sa.String(50), index=True, nullable=False, comment="物料号")
    name = sa.Column(sa.String(50), index=True, nullable=False, comment="物料名称")
    record_id = sa.Column(sa.ForeignKey("tb_material_record.id"), comment="关联存货档案")



class ProductMaterial(Base):
    __tablename__ = "tb_warehouse_product"
    __table_args__ = ({"comment": "产品物料表"},)

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    create_time = sa.Column(sa.DateTime, default=datetime.now)
    update_time = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)

    number = sa.Column(sa.String(50), index=True, nullable=False, comment="物料号")
    name = sa.Column(sa.String(50), index=True, nullable=False, comment="物料名称")
    record_id = sa.Column(sa.ForeignKey("tb_material_record.id"), comment="关联存货档案")


class MaterialEntity(Base):
    __tablename__ = "tb_material_entity"
    __table_args__ = ({"comment": "材料表"},)

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    create_time = sa.Column(sa.DateTime, default=datetime.now)
    update_time = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)

    # TODO 因为材料编码跟二维码字串绑定，长度再待确认
    entity_no = sa.Column(sa.String(1024), comment="材料编号")
    attr_id = sa.Column(sa.ForeignKey("tb_material_attr_value.id"), comment="关联属性表")
    # TODO 连接到物料表，是否使用外键待定
    material_num = sa.Column(sa.String(50), comment="物料号")
    material_record_id = sa.Column(
        sa.ForeignKey("tb_material_record.id"), comment="关联库存档案表"
    )
    # TODO String长度
    batch_no = sa.Column(sa.String(50), comment="批次编号")
    batch_id = sa.Column(sa.ForeignKey("tb_material_batch.id"), comment="关联批次表")
    iquantity = sa.Column(sa.DECIMAL(20, 6), comment="计量数量")
    # 暂时只有可分割(无标签),不可分割(有标签)
    entity_type = sa.Column(sa.Integer, comment="材料类型,暂时(有标签/无标签)")
    warehouse_id = sa.Column(sa.ForeignKey("tb_warehouse.id"), comment="关联仓库表")
    warehouse_status = sa.Column(sa.Integer, comment="仓储状态")


class MaterialBatch(Base):
    __tablename__ = "tb_material_batch"
    __table_args__ = ({"comment": "到货批次表"},)

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    create_time = sa.Column(sa.DateTime, default=datetime.now)
    update_time = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)

    # 任何批次都必须有物料号
    material_num = sa.Column(sa.String(50), comment="物料号", nullable=False)
    material_record_id = sa.Column(sa.ForeignKey("tb_material_record.id"))
    batch_no = sa.Column(sa.String(50), comment="批次编号")
    purchase_record_id = sa.Column(
        sa.ForeignKey("tb_purchase_record.id"), comment="关联进货单表"
    )
    # TODO String 长度
    purchase_record_no = sa.Column(sa.String(50), comment="到货单号")

    dp_date = sa.Column(sa.DateTime, default=datetime.now, comment="生产日期")
    imass_date = sa.Column(sa.Integer, comment="保质期")
    iquantity = sa.Column(
        sa.DECIMAL(20, 6), comment="计量数量"
    )  # 对应tb_warehouse_raw_material.min_unit_total
    cinvm_unit = sa.Column(
        sa.String(10), comment="计量单位"
    )  # 对应tb_warehouse_raw_material.unit
    bgsp = sa.Column(sa.Boolean, comment="是否检验")
    # TODO 待定
    binspect = sa.Column(sa.Boolean, comment="是否已报检")
    iqc_inspect_id = sa.Column(sa.ForeignKey("tb_iqc_inspect.id"), comment="质检单号")


class IQCInspect(Base):
    __tablename__ = "tb_iqc_inspect"  # 质检单表
    __table_args__ = ({"comment": "质检单表"},)

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    create_time = sa.Column(sa.DateTime, default=datetime.now)
    update_time = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)

    iqc_standard_id = sa.Column(
        sa.ForeignKey("tb_quality_standard_manage.id"), comment="质检规格"
    )
    batch_id = sa.Column(sa.ForeignKey("tb_material_batch.id"), comment="关联批次表")

    sample_iquantity = sa.Column(sa.DECIMAL(20, 6), comment="抽样数量")
    ok_iquantity = sa.Column(sa.DECIMAL(20, 6), comment="质检ok数量")
    # TODO ng = sample - ok
    ng_iquantity = sa.Column(sa.DECIMAL(20, 6), comment="质检ng数量")

    #  disagree_iquantity = batch_iquantity - agree_iquantity
    batch_iquantity = sa.Column(sa.DECIMAL(20, 6), comment="批次总数量")
    agree_iquantity = sa.Column(sa.DECIMAL(20, 6), comment="允收数量")
    disagree_iquantity = sa.Column(sa.DECIMAL(20, 6), comment="允收数量")

    creator_id = sa.Column(sa.ForeignKey("tb_user.id"), comment="关联创建记录人")
    creator_username = sa.Column(sa.String(50), comment="创建人名")
    reviewer_id = sa.Column(sa.ForeignKey("tb_user.id"), comment="关联审批人")
    reviewer_username = sa.Column(sa.String(50), comment="审批人名")

    inspect_status = sa.Column(sa.Integer, comment="质检状态")
    review_handle = sa.Column(sa.Integer, comment="处理方式")

    iqc_time = sa.Column(sa.DateTime, comment="质检时间")
    review_time = sa.Column(sa.DateTime, comment="审核时间")


class PurchaseRecord(Base):
    __tablename__ = "tb_purchase_record"
    __table_args__ = ({"comment": "进货单表"},)

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    create_time = sa.Column(sa.DateTime, default=datetime.now)
    update_time = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)

    record_no = sa.Column(sa.String(50), comment="到货单号")
    bus_type = sa.Column(sa.String(50), comment="业务类型")
    record_date = sa.Column(sa.DateTime)
    ven_code = sa.Column(sa.String(50), comment="供应商编码")
    batches = relationship("MaterialBatch", backref="purchase_record")


class WarehouseCheckin(Base):

    __tablename__ = "tb_warehouse_checkin"
    __table_args__ = ({"comment": "入库单主表"},)

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    create_time = sa.Column(sa.DateTime, default=datetime.now)
    update_time = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)
    record_no = sa.Column(sa.String(50), comment="入库单号")
    checkin_type = sa.Column(sa.Integer, comment="入库类型")
    warehouse_id = sa.Column(sa.ForeignKey("tb_warehouse.id"), comment="关联仓库表")
    creator_id = sa.Column(sa.ForeignKey("tb_user.id"), comment="关联创建人")
    reviewer_id = sa.Column(sa.ForeignKey("tb_user.id"), comment="关联审核人")


class WarehouseMaterialCheckin(Base):

    __tablename__ = "tb_warehouse_material_checkin"
    __table_args__ = ({"comment": "原材料入库单表"},)

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    create_time = sa.Column(sa.DateTime, default=datetime.now)
    update_time = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)
    record_no = sa.Column(sa.String(50), comment="入库单号")
    checkin_type = sa.Column(sa.Integer, comment="入库类型")
    warehouse_id = sa.Column(sa.ForeignKey("tb_warehouse.id"), comment="关联仓库表")
    purchase_record_id = sa.Column(sa.ForeignKey("tb_purchase_record.id"))
    material_entity_id = sa.Column(sa.ForeignKey("tb_material_entity.id"))
    material_record_id = sa.Column(sa.ForeignKey("tb_material_record.id"))
    total_iquantity = sa.Column(sa.DECIMAL(20, 6), comment="批次入库数量")


class WarehouseStorage(Base):

    __tablename__ = "tb_warehouse_storage"
    __table_args__ = ({"comment": "库存流水表"},)

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    material_entity_id = sa.Column(
        sa.ForeignKey("tb_material_entity.id"), comment="材料编号,关联材料表具体材料"
    )
    create_time = sa.Column(sa.DateTime, default=datetime.now)
    update_time = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)
    shelf_id = sa.Column(sa.ForeignKey("tb_warehouse_goods_shelf.id"), comment="关联货架表")
    shelf_location = sa.Column(sa.String(50), comment="货位信息")
    iquantity = sa.Column(sa.DECIMAL(20, 6), comment="出入库流水数量")
    checkin_type = sa.Column(sa.Integer, comment="出入库类型")
    record_no = sa.Column(sa.String(50), comment="出入库单号")
    warehouse_id = sa.Column(sa.ForeignKey("tb_warehouse.id"), comment="关联仓库表")
    batch_no = sa.Column(sa.String(50), comment="批号编码")


class WarehouseCheckout(Base):

    __tablename__ = "tb_warehouse_checkout"
    __table_args__ = ({"comment": "出库单主表"},)

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    create_time = sa.Column(sa.DateTime, default=datetime.now)
    update_time = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)
    record_no = sa.Column(sa.String(50), comment="出库单号")
    checkout_type = sa.Column(sa.Integer, comment="出库类型")
    warehouse_id = sa.Column(sa.ForeignKey("tb_warehouse.id"), comment="关联仓库表")
    creator_id = sa.Column(sa.ForeignKey("tb_user.id"), comment="关联创建人")
    reviewer_id = sa.Column(sa.ForeignKey("tb_user.id"), comment="关联审核人")
    dept_id = sa.Column(sa.ForeignKey("tb_department.id"), comment="关联领用部门")


class WarehouseMaterialCheckout(Base):
    __tablename__ = "tb_warehouse_material_checkout"
    __table_args__ = ({"comment": "原材料出库单表"},)

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    create_time = sa.Column(sa.DateTime, default=datetime.now)
    update_time = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)
    record_no = sa.Column(sa.String(50), comment="入库单号")
    checkin_type = sa.Column(sa.Integer, comment="入库类型")
    warehouse_id = sa.Column(sa.ForeignKey("tb_warehouse.id"), comment="关联仓库表")
    material_record_id = sa.Column(sa.ForeignKey("tb_material_record.id"))
    total_iquantity = sa.Column(sa.DECIMAL(20, 6), comment="批次入库数量")


class WarehouseSchedule(Base):
    __tablename__ = "tb_warehouse_transfer"
    __table_args__ = ({"comment": "调拨单表"},)

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    create_time = sa.Column(sa.DateTime, default=datetime.now)
    update_time = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)
    warehouse_id = sa.Column(sa.ForeignKey("tb_warehouse.id"), comment="转入仓库，关联仓库表")
    transfer_warehouse_id = sa.Column(
        sa.ForeignKey("tb_warehouse.id"), comment="转出仓库,关联仓库表"
    )
    # TODO 确认生产单id关联关系
    ipro_order_id = sa.Column(
        sa.ForeignKey("tb_braid_plan_schedule.id"), comment="关联生产单表"
    )
    transfer_status = sa.Column(sa.Integer, comment="调拨状态")


class MaterialAttributeName(Base):
    __tablename__ = "tb_material_attr_name"
    __table_args__ = ({"comment": "库存key表"},)

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    create_time = sa.Column(sa.DateTime, default=datetime.now)
    update_time = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)
    material_record_id = sa.Column(
        sa.ForeignKey("tb_material_record.id"), unique=True, comment="关联物料档案表"
    )
    keys = sa.Column(sa.String(1024), comment="明细模板字段名(逗号分割)")
    is_locked = sa.Column(sa.Boolean, comment="是否锁定不许更改")


class MaterialAttributeValue(Base):
    __tablename__ = "tb_material_attr_value"
    __table_args__ = ({"comment": "库存value表"},)

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    create_time = sa.Column(sa.DateTime, default=datetime.now)
    update_time = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)
    values = sa.Column(sa.String(1024), comment="明细模板字段值(逗号分割)")
    batch_id = sa.Column(sa.ForeignKey("tb_material_batch.id"), comment="关联批次表")





def main():
    Base.metadata.create_all(db)


if __name__ == "__main__":
    main()
