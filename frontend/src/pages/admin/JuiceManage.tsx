import { useEffect, useState } from 'react';
import { Table, Button, Modal, Form, Input, Select, Space, message, Popconfirm } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { getJuices } from '../../api/juice';
import type { JuiceItem } from '../../api/juice';
import { getBrands } from '../../api/brand';
import type { BrandItem } from '../../api/brand';
import { getTags, adminCreateJuice, adminUpdateJuice, adminDeleteJuice } from '../../api/admin';

export default function JuiceManage() {
  const [juices, setJuices] = useState<JuiceItem[]>([]);
  const [brands, setBrands] = useState<BrandItem[]>([]);
  const [tags, setTags] = useState<{ id: number; name: string }[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<JuiceItem | null>(null);
  const [form] = Form.useForm();

  const fetchData = async () => {
    setLoading(true);
    try {
      const [jRes, bRes, tRes] = await Promise.all([
        getJuices({ page: 1, size: 100 }),
        getBrands({ page: 1, size: 100 }),
        getTags(),
      ]);
      setJuices(jRes.data.data.items);
      setBrands(bRes.data.data.items);
      setTags(tRes.data.data);
    } finally { setLoading(false); }
  };

  useEffect(() => { fetchData(); }, []);

  const openCreate = () => { setEditing(null); form.resetFields(); setModalOpen(true); };
  const openEdit = (juice: JuiceItem) => {
    setEditing(juice);
    form.setFieldsValue({ ...juice, tag_ids: juice.tags.map((t) => t.id) });
    setModalOpen(true);
  };

  const handleSubmit = async () => {
    const values = await form.validateFields();
    if (editing) {
      await adminUpdateJuice(editing.id, values);
      message.success('更新成功');
    } else {
      await adminCreateJuice(values);
      message.success('创建成功');
    }
    setModalOpen(false);
    fetchData();
  };

  const handleDelete = async (id: number) => {
    await adminDeleteJuice(id);
    message.success('删除成功');
    fetchData();
  };

  const columns = [
    { title: 'ID', dataIndex: 'id', width: 60 },
    { title: '名称', dataIndex: 'name' },
    { title: '品牌', dataIndex: 'brand_name', width: 120 },
    { title: '评分', dataIndex: 'avg_rating', width: 80, render: (v: number) => v.toFixed(1) },
    {
      title: '操作', width: 160, render: (_: unknown, record: JuiceItem) => (
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
        <h2 className="text-xl font-bold">烟油管理</h2>
        <Button type="primary" icon={<PlusOutlined />} onClick={openCreate}>新建烟油</Button>
      </div>
      <Table columns={columns} dataSource={juices} rowKey="id" loading={loading} pagination={false} />
      <Modal title={editing ? '编辑烟油' : '新建烟油'} open={modalOpen} onOk={handleSubmit} onCancel={() => setModalOpen(false)} destroyOnClose width={600}>
        <Form form={form} layout="vertical">
          <Form.Item name="brand_id" label="品牌" rules={[{ required: true }]}>
            <Select options={brands.map((b) => ({ label: b.name, value: b.id }))} />
          </Form.Item>
          <Form.Item name="name" label="名称" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="flavor_profile" label="味型"><Input /></Form.Item>
          <Form.Item name="nicotine_range" label="尼古丁含量"><Input /></Form.Item>
          <Form.Item name="vg_pg_ratio" label="VG/PG"><Input /></Form.Item>
          <Form.Item name="volume" label="容量"><Input /></Form.Item>
          <Form.Item name="price_range" label="参考价格"><Input /></Form.Item>
          <Form.Item name="description" label="描述"><Input.TextArea /></Form.Item>
          <Form.Item name="tag_ids" label="口味标签">
            <Select mode="multiple" options={tags.map((t) => ({ label: t.name, value: t.id }))} />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}
