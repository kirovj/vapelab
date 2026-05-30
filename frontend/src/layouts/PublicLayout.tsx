import { Outlet, Link, useNavigate } from 'react-router-dom';
import { Layout, Menu, Input, Button, Space } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import { useAuthStore } from '../stores/authStore';

const { Header, Content, Footer } = Layout;

export default function PublicLayout() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  return (
    <Layout className="min-h-screen">
      <Header className="flex items-center justify-between bg-white shadow-sm px-6">
        <div className="flex items-center gap-8">
          <Link to="/" className="text-xl font-bold text-gray-800">
            雾室 vapelab
          </Link>
          <Menu
            mode="horizontal"
            className="border-none"
            items={[
              { key: 'brands', label: '品牌', onClick: () => navigate('/brands') },
              { key: 'juices', label: '烟油', onClick: () => navigate('/juices') },
            ]}
          />
        </div>
        <Space>
          <Input
            prefix={<SearchOutlined />}
            placeholder="搜索烟油..."
            onPressEnter={(e) =>
              navigate(`/search?q=${encodeURIComponent((e.target as HTMLInputElement).value)}`)
            }
          />
          {user ? (
            <Space>
              <Button type="link" onClick={() => navigate('/me')}>
                {user.username}
              </Button>
              <Button onClick={logout}>退出</Button>
            </Space>
          ) : (
            <Space>
              <Button onClick={() => navigate('/login')}>登录</Button>
              <Button type="primary" onClick={() => navigate('/register')}>
                注册
              </Button>
            </Space>
          )}
        </Space>
      </Header>
      <Content className="p-6 max-w-7xl mx-auto w-full">
        <Outlet />
      </Content>
      <Footer className="text-center text-gray-400">
        雾室 vapelab — 电子烟油评分社区
      </Footer>
    </Layout>
  );
}
