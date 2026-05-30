import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Spin, Descriptions, Row, Col, Empty } from 'antd';
import { getBrand } from '../api/brand';
import type { BrandItem } from '../api/brand';
import { getJuices } from '../api/juice';
import type { JuiceItem } from '../api/juice';
import JuiceCard from '../components/JuiceCard';

export default function BrandDetail() {
  const { id } = useParams<{ id: string }>();
  const [brand, setBrand] = useState<BrandItem | null>(null);
  const [juices, setJuices] = useState<JuiceItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    Promise.all([
      getBrand(Number(id)),
      getJuices({ page: 1, size: 50, brand_id: Number(id) }),
    ])
      .then(([bRes, jRes]) => {
        setBrand(bRes.data.data);
        setJuices(jRes.data.data.items);
      })
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <Spin size="large" className="block text-center mt-12" />;
  if (!brand) return <Empty description="品牌不存在" />;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">{brand.name}</h1>
      <Descriptions bordered column={{ xs: 1, sm: 2 }} className="mb-8">
        <Descriptions.Item label="国家">{brand.country}</Descriptions.Item>
        <Descriptions.Item label="烟油数量">{brand.juice_count}</Descriptions.Item>
        {brand.description && (
          <Descriptions.Item label="品牌描述" span={2}>{brand.description}</Descriptions.Item>
        )}
      </Descriptions>

      <h2 className="text-xl font-bold mb-4">旗下烟油</h2>
      {juices.length === 0 ? (
        <Empty description="暂无烟油" />
      ) : (
        <Row gutter={[16, 16]}>
          {juices.map((j) => (
            <Col key={j.id} xs={24} sm={12} md={8} lg={6}>
              <JuiceCard juice={j} />
            </Col>
          ))}
        </Row>
      )}
    </div>
  );
}
