import { useEffect, useState } from 'react';
import { Table, Button, message, Switch, Space } from 'antd';
import { adminGetUsers, adminToggleUserActive } from '../../api/admin';

interface UserItem {
  id: number;
  username: string;
  email: string;
  is_admin: boolean;
  is_active: boolean;
  created_at: string;
}

export default function UserManage() {
  const [users, setUsers] = useState<UserItem[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const res = await adminGetUsers();
      setUsers(res.data.data);
    } finally { setLoading(false); }
  };

  useEffect(() => { fetchUsers(); }, []);

  const toggleActive = async (id: number) => {
    try {
      await adminToggleUserActive(id);
      message.success('操作成功');
      fetchUsers();
    } catch { message.error('操作失败'); }
  };

  const columns = [
    { title: 'ID', dataIndex: 'id', width: 60 },
    { title: '用户名', dataIndex: 'username' },
    { title: '邮箱', dataIndex: 'email' },
    { title: '角色', dataIndex: 'is_admin', width: 80, render: (v: boolean) => v ? '管理员' : '用户' },
    { title: '状态', dataIndex: 'is_active', width: 80, render: (v: boolean, record: UserItem) => (
      <Switch checked={v} onChange={() => toggleActive(record.id)} checkedChildren="正常" unCheckedChildren="禁用" />
    )},
    { title: '注册时间', dataIndex: 'created_at', width: 120, render: (v: string) => v ? new Date(v).toLocaleDateString('zh-CN') : '-' },
  ];

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">用户管理</h2>
      <Space style={{ marginBottom: 16 }}>
        <Button type="primary" onClick={fetchUsers}>刷新</Button>
      </Space>
      <Table columns={columns} dataSource={users} rowKey="id" loading={loading} pagination={false} />
    </div>
  );
}
