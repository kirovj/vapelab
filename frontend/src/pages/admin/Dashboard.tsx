import { useEffect, useState } from 'react';
import { Card, Row, Col, Statistic } from 'antd';
import { ExperimentOutlined, TagOutlined } from '@ant-design/icons';
import { getBrands } from '../../api/brand';
import { getJuices } from '../../api/juice';

export default function Dashboard() {
  const [stats, setStats] = useState({ brands: 0, juices: 0 });

  useEffect(() => {
    getBrands({ page: 1, size: 1 }).then((r) => setStats((s) => ({ ...s, brands: r.data.data.total })));
    getJuices({ page: 1, size: 1 }).then((r) => setStats((s) => ({ ...s, juices: r.data.data.total })));
  }, []);

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">仪表盘</h2>
      <Row gutter={16}>
        <Col span={8}>
          <Card><Statistic title="品牌数" value={stats.brands} prefix={<TagOutlined />} /></Card>
        </Col>
        <Col span={8}>
          <Card><Statistic title="烟油数" value={stats.juices} prefix={<ExperimentOutlined />} /></Card>
        </Col>
      </Row>
    </div>
  );
}
