import { useEffect, useState } from 'react';
import { Table, Button, Modal, Form, Input, Space, message, Popconfirm } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { getBrands } from '../../api/brand';
import type { BrandItem } from '../../api/brand';
import { adminCreateBrand, adminUpdateBrand, adminDeleteBrand } from '../../api/admin';

export default function BrandManage() {
  const [brands, setBrands] = useState<BrandItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<BrandItem | null>(null);
  const [form] = Form.useForm();

  const fetchBrands = async () => {
    setLoading(true);
    try { const res = await getBrands({ page: 1, size: 100 }); setBrands(res.data.data.items); }
    finally { setLoading(false); }
  };

  useEffect(() => { fetchBrands(); }, []);

  const openCreate = () => { setEditing(null); form.resetFields(); setModalOpen(true); };
  const openEdit = (brand: BrandItem) => { setEditing(brand); form.setFieldsValue(brand); setModalOpen(true); };

  const handleSubmit = async () => {
    const values = await form.validateFields();
    if (editing) {
      await adminUpdateBrand(editing.id, values);
      message.success('更新成功');
    } else {
      await adminCreateBrand(values);
      message.success('创建成功');
    }
    setModalOpen(false);
    fetchBrands();
  };

  const handleDelete = async (id: number) => {
    await adminDeleteBrand(id);
    message.success('删除成功');
    fetchBrands();
  };

  const columns = [
    { title: 'ID', dataIndex: 'id', width: 60 },
    { title: '名称', dataIndex: 'name' },
    { title: '国家', dataIndex: 'country', width: 100 },
    { title: '烟油数', dataIndex: 'juice_count', width: 80 },
    {
      title: '操作', width: 160, render: (_: unknown, record: BrandItem) => (
        <Space>
          <Button size="small" icon={<EditOutlined />} onClick={() => openEdit(record)}>编辑</Button>
          <Popconfirm title="确定删除？" onConfirm={() => handleDelete(record.id)}>
            <Button size="small" danger icon={<DeleteOutlined />}>删除</Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">品牌管理</h2>
        <Button type="primary" icon={<PlusOutlined />} onClick={openCreate}>新建品牌</Button>
      </div>
      <Table columns={columns} dataSource={brands} rowKey="id" loading={loading} pagination={false} />
      <Modal title={editing ? '编辑品牌' : '新建品牌'} open={modalOpen} onOk={handleSubmit} onCancel={() => setModalOpen(false)} destroyOnClose>
        <Form form={form} layout="vertical">
          <Form.Item name="name" label="品牌名称" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="country" label="国家" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="description" label="描述"><Input.TextArea /></Form.Item>
        </Form>
      </Modal>
    </div>
  );
}
