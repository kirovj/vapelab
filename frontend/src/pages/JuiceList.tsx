import { useEffect, useState } from 'react';
import { Row, Col, Select, Spin } from 'antd';
import { getJuices } from '../api/juice';
import type { JuiceItem } from '../api/juice';
import JuiceCard from '../components/JuiceCard';

const FLAVOR_OPTIONS = [
  { label: '水果', value: '水果' }, { label: '甜点', value: '甜点' },
  { label: '烟草', value: '烟草' }, { label: '薄荷', value: '薄荷' }, { label: '饮品', value: '饮品' },
];

const SORT_OPTIONS = [
  { label: '最新', value: 'newest' }, { label: '评分最高', value: 'rating_desc' }, { label: '评分最低', value: 'rating_asc' },
];

export default function JuiceList() {
  const [juices, setJuices] = useState<JuiceItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [flavor, setFlavor] = useState<string | undefined>();
  const [sort, setSort] = useState('newest');

  const fetchJuices = async () => {
    setLoading(true);
    try {
      const res = await getJuices({ page: 1, size: 50, flavor_profile: flavor, sort });
      setJuices(res.data.data.items);
    } finally { setLoading(false); }
  };

  useEffect(() => { fetchJuices(); }, [flavor, sort]);

  return (
    <div>
      <div className="mb-4 flex gap-4">
        <Select allowClear placeholder="味型筛选" style={{ width: 150 }} value={flavor} onChange={setFlavor} options={FLAVOR_OPTIONS} />
        <Select style={{ width: 150 }} value={sort} onChange={setSort} options={SORT_OPTIONS} />
      </div>
      {loading ? <Spin size="large" className="block text-center mt-12" /> : (
        <Row gutter={[16, 16]}>
          {juices.map((j) => (<Col key={j.id} xs={24} sm={12} md={8} lg={6}><JuiceCard juice={j} /></Col>))}
        </Row>
      )}
    </div>
  );
}
