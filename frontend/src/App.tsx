import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import PublicLayout from './layouts/PublicLayout';
import AdminLayout from './layouts/AdminLayout';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import BrandList from './pages/BrandList';
import BrandDetail from './pages/BrandDetail';
import JuiceList from './pages/JuiceList';
import JuiceDetail from './pages/JuiceDetail';
import Profile from './pages/Profile';
import Search from './pages/Search';
import Submit from './pages/Submit';
import SubmissionManage from './pages/admin/SubmissionManage';
import Dashboard from './pages/admin/Dashboard';
import BrandManage from './pages/admin/BrandManage';
import JuiceManage from './pages/admin/JuiceManage';
import UserManage from './pages/admin/UserManage';

function App() {
  return (
    <ConfigProvider locale={zhCN}>
      <BrowserRouter>
        <Routes>
          <Route element={<PublicLayout />}>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/search" element={<Search />} />
            <Route path="/me" element={<Profile />} />
            <Route path="/register" element={<Register />} />
            <Route path="/brands" element={<BrandList />} />
            <Route path="/brands/:id" element={<BrandDetail />} />
            <Route path="/juices" element={<JuiceList />} />
            <Route path="/juices/:id" element={<JuiceDetail />} />
            <Route path="/submit" element={<Submit />} />
          </Route>
          <Route path="/admin" element={<AdminLayout />}>
            <Route index element={<Dashboard />} />
            <Route path="brands" element={<BrandManage />} />
            <Route path="juices" element={<JuiceManage />} />
            <Route path="users" element={<UserManage />} />
            <Route path="submissions" element={<SubmissionManage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ConfigProvider>
  );
}

export default App;
