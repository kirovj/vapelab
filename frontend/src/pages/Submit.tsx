import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Form, Input, Select, Button, message } from 'antd';
import { getBrands } from '../api/brand';
import type { BrandItem } from '../api/brand';
import { getTags } from '../api/admin';
import client from '../api/client';

export default function Submit() {
  const [brands, setBrands] = useState<BrandItem[]>([]);
  const [tags, setTags] = useState<{ id: number; name: string }[]>([]);
  const [loading, setLoading] = useState(false);
  const [form] = Form.useForm();
  const navigate = useNavigate();

  useEffect(() => {
    getBrands({ page: 1, size: 100 }).then((r) => setBrands(r.data.data.items));
    getTags().then((r) => setTags(r.data.data));
  }, []);

  const handleSubmit = async (values: Record<string, unknown>) => {
    setLoading(true);
    try {
      await client.post('/submissions/create', { ...values, tag_ids: values.tag_ids || [] });
      message.success('提交成功，等待管理员审核');
      navigate('/me');
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || '提交失败';
      message.error(msg);
    } finally { setLoading(false); }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">提交新烟油</h1>
      <Card>
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          <Form.Item name="brand_id" label="品牌" rules={[{ required: true, message: '请选择品牌' }]}>
            <Select
              showSearch
              placeholder="选择品牌"
              filterOption={(input, option) => (option?.label as string || '').includes(input)}
              options={brands.map((b) => ({ label: b.name, value: b.id }))}
            />
          </Form.Item>
          <Form.Item name="name" label="烟油名称" rules={[{ required: true, message: '请输入名称' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="flavor_profile" label="味型">
            <Select
              allowClear
              placeholder="选择味型"
              options={[
                { label: '水果', value: '水果' },
                { label: '甜点', value: '甜点' },
                { label: '烟草', value: '烟草' },
                { label: '薄荷', value: '薄荷' },
                { label: '饮品', value: '饮品' },
              ]}
            />
          </Form.Item>
          <Form.Item name="nicotine_range" label="尼古丁含量">
            <Input placeholder="如 0/3/6mg" />
          </Form.Item>
          <Form.Item name="vg_pg_ratio" label="VG/PG">
            <Input placeholder="如 70/30" />
          </Form.Item>
          <Form.Item name="volume" label="容量">
            <Input placeholder="如 60ml" />
          </Form.Item>
          <Form.Item name="price_range" label="参考价格">
            <Input placeholder="如 $12-$18" />
          </Form.Item>
          <Form.Item name="description" label="口味描述">
            <Input.TextArea rows={4} />
          </Form.Item>
          <Form.Item name="tag_ids" label="口味标签">
            <Select mode="multiple" placeholder="选择标签" options={tags.map((t) => ({ label: t.name, value: t.id }))} />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading}>提交审核</Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
}
