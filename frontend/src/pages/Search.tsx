import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Row, Col, Spin, Empty } from 'antd';
import { searchJuices, getJuices } from '../api/juice';
import type { JuiceItem } from '../api/juice';
import JuiceCard from '../components/JuiceCard';
import FilterPanel from '../components/FilterPanel';

/** 搜索页面：支持关键词搜索和味型/排序筛选 */
export default function Search() {
  const [searchParams] = useSearchParams();
  const q = searchParams.get('q') || '';
  const [juices, setJuices] = useState<JuiceItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [flavor, setFlavor] = useState<string | undefined>();
  const [sort, setSort] = useState('newest');

  useEffect(() => {
    setLoading(true);
    const fetcher = q
      ? searchJuices(q, 1, 50)
      : getJuices({ page: 1, size: 50, flavor_profile: flavor, sort });
    fetcher.then((res) => setJuices(res.data.data.items)).finally(() => setLoading(false));
  }, [q, flavor, sort]);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">{q ? `搜索: ${q}` : '浏览烟油'}</h1>
      <FilterPanel flavor={flavor} onFlavorChange={setFlavor} sort={sort} onSortChange={setSort} />
      {loading ? (
        <Spin size="large" className="block text-center mt-12" />
      ) : juices.length === 0 ? (
        <Empty description="没有找到相关烟油" />
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
