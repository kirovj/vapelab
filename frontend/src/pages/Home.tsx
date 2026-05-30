import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Row, Col, Input, Spin } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import { getBrands } from '../api/brand';
import type { BrandItem } from '../api/brand';
import { getTopRated } from '../api/juice';
import type { JuiceItem } from '../api/juice';
import BrandCard from '../components/BrandCard';
import JuiceCard from '../components/JuiceCard';

/** 首页：展示热门品牌、高分烟油和搜索入口 */
export default function Home() {
  const [brands, setBrands] = useState<BrandItem[]>([]);
  const [topJuices, setTopJuices] = useState<JuiceItem[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    Promise.all([
      getBrands({ page: 1, size: 6 }),
      getTopRated(8),
    ]).then(([bRes, jRes]) => {
      setBrands(bRes.data.data.items);
      setTopJuices(jRes.data.data);
    }).finally(() => setLoading(false));
  }, []);

  const handleSearch = (value: string) => {
    if (value.trim()) navigate(`/search?q=${encodeURIComponent(value.trim())}`);
  };

  if (loading) return <Spin size="large" className="block text-center mt-12" />;

  return (
    <div>
      <div className="text-center py-12">
        <h1 className="text-3xl font-bold mb-4">发现你的下一款心头好</h1>
        <p className="text-gray-500 mb-8">浏览全球电子烟油品牌，查看真实用户评分</p>
        <Input.Search
          size="large"
          placeholder="搜索烟油名称、品牌..."
          prefix={<SearchOutlined />}
          onSearch={handleSearch}
          style={{ maxWidth: 500 }}
          enterButton
        />
      </div>

      {brands.length > 0 && (
        <section className="mb-8">
          <h2 className="text-xl font-bold mb-4">热门品牌</h2>
          <Row gutter={[16, 16]}>
            {brands.map((b) => (<Col key={b.id} xs={12} sm={8} md={4}><BrandCard brand={b} /></Col>))}
          </Row>
        </section>
      )}

      {topJuices.length > 0 && (
        <section>
          <h2 className="text-xl font-bold mb-4">高分烟油</h2>
          <Row gutter={[16, 16]}>
            {topJuices.map((j) => (<Col key={j.id} xs={24} sm={12} md={8} lg={6}><JuiceCard juice={j} /></Col>))}
          </Row>
        </section>
      )}
    </div>
  );
}
