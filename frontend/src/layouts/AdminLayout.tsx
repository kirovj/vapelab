import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import {
  DashboardOutlined,
  TagOutlined,
  ExperimentOutlined,
  FileProtectOutlined,
  UserOutlined,
} from '@ant-design/icons';

const { Sider, Content } = Layout;

const menuItems = [
  { key: '/admin', icon: <DashboardOutlined />, label: '仪表盘' },
  { key: '/admin/brands', icon: <TagOutlined />, label: '品牌管理' },
  { key: '/admin/juices', icon: <ExperimentOutlined />, label: '烟油管理' },
  { key: '/admin/submissions', icon: <FileProtectOutlined />, label: '审核管理' },
  { key: '/admin/users', icon: <UserOutlined />, label: '用户管理' },
];

export default function AdminLayout() {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <Layout className="min-h-screen">
      <Sider width={200} className="bg-white">
        <div className="h-16 flex items-center justify-center font-bold text-lg">
          管理后台
        </div>
        <Menu
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
        />
      </Sider>
      <Content className="p-6">
        <Outlet />
      </Content>
    </Layout>
  );
}
