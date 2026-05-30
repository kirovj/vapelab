import { useEffect, useState } from 'react';
import { Tabs, Card, Descriptions, Button, Form, Input, message, Spin, Empty } from 'antd';
import { getMyProfile, updateProfile } from '../api/user';
import type { UserProfile } from '../api/user';
import { useAuthStore } from '../stores/authStore';
import { useNavigate } from 'react-router-dom';

export default function Profile() {
  const { logout } = useAuthStore();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [form] = Form.useForm();
  const navigate = useNavigate();

  /** 获取用户信息 */
  const fetchProfile = async () => {
    setLoading(true);
    try {
      const res = await getMyProfile();
      setProfile(res.data.data);
    } catch {
      // 未登录
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  /** 更新用户资料 */
  const handleUpdate = async (values: { username: string; email: string }) => {
    try {
      await updateProfile(values);
      message.success('资料更新成功');
      setEditing(false);
      fetchProfile();
    } catch {
      message.error('更新失败');
    }
  };

  if (loading) return <Spin size="large" className="block text-center mt-12" />;
  if (!profile) return <Empty description="请先登录" />;

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">个人中心</h1>

      <Card className="mb-6">
        {editing ? (
          <Form form={form} layout="vertical" initialValues={profile} onFinish={handleUpdate}>
            <Form.Item name="username" label="用户名" rules={[{ required: true }]}>
              <Input />
            </Form.Item>
            <Form.Item name="email" label="邮箱" rules={[{ required: true, type: 'email' }]}>
              <Input />
            </Form.Item>
            <Form.Item>
              <Button type="primary" htmlType="submit" className="mr-2">
                保存
              </Button>
              <Button onClick={() => setEditing(false)}>取消</Button>
            </Form.Item>
          </Form>
        ) : (
          <>
            <Descriptions column={1}>
              <Descriptions.Item label="用户名">{profile.username}</Descriptions.Item>
              <Descriptions.Item label="邮箱">{profile.email}</Descriptions.Item>
              <Descriptions.Item label="角色">
                {profile.is_admin ? '管理员' : '普通用户'}
              </Descriptions.Item>
            </Descriptions>
            <div className="mt-4">
              <Button
                onClick={() => {
                  form.setFieldsValue(profile);
                  setEditing(true);
                }}
                className="mr-2"
              >
                编辑资料
              </Button>
              <Button
                danger
                onClick={() => {
                  logout();
                  navigate('/');
                }}
              >
                退出登录
              </Button>
            </div>
          </>
        )}
      </Card>

      <Tabs
        items={[
          {
            key: 'reviews',
            label: '我的评论',
            children: <div className="text-gray-400 text-center py-8">评论功能即将上线</div>,
          },
          {
            key: 'submissions',
            label: '我的提交',
            children: <div className="text-gray-400 text-center py-8">提交记录即将上线</div>,
          },
        ]}
      />
    </div>
  );
}
