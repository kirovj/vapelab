import { useEffect, useState } from 'react';
import { Table, Button, Space, message } from 'antd';
import { CheckOutlined, CloseOutlined } from '@ant-design/icons';
import client from '../../api/client';

interface SubmissionItem {
  id: number;
  brand_name: string;
  name: string;
  flavor_profile: string | null;
  status: string;
  created_at: string;
}

export default function SubmissionManage() {
  const [submissions, setSubmissions] = useState<SubmissionItem[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await client.get('/admin/submissions');
      setSubmissions(res.data.data);
    } finally { setLoading(false); }
  };

  useEffect(() => { fetchData(); }, []);

  const handleApprove = async (id: number) => {
    await client.post(`/admin/submissions/${id}/approve`);
    message.success('审核通过');
    fetchData();
  };

  const handleReject = async (id: number) => {
    await client.post(`/admin/submissions/${id}/reject`);
    message.success('已拒绝');
    fetchData();
  };

  const columns = [
    { title: 'ID', dataIndex: 'id', width: 60 },
    { title: '名称', dataIndex: 'name' },
    { title: '品牌', dataIndex: 'brand_name', width: 120 },
    { title: '味型', dataIndex: 'flavor_profile', width: 80 },
    {
      title: '提交时间', dataIndex: 'created_at', width: 120,
      render: (v: string) => v ? new Date(v).toLocaleDateString('zh-CN') : '-',
    },
    {
      title: '操作', width: 160,
      render: (_: unknown, record: SubmissionItem) => (
        <Space>
          <Button type="primary" size="small" icon={<CheckOutlined />} onClick={() => handleApprove(record.id)}>通过</Button>
          <Button danger size="small" icon={<CloseOutlined />} onClick={() => handleReject(record.id)}>拒绝</Button>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">审核管理</h2>
      <Table columns={columns} dataSource={submissions} rowKey="id" loading={loading} pagination={false} />
    </div>
  );
}
