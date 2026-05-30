import { useEffect, useState } from 'react';
import { Row, Col, Select, Spin } from 'antd';
import { getBrands } from '../api/brand';
import type { BrandItem } from '../api/brand';
import BrandCard from '../components/BrandCard';

const COUNTRY_OPTIONS = [
  { label: '美国', value: 'USA' },
  { label: '中国', value: 'CN' },
  { label: '日本', value: 'JP' },
  { label: '英国', value: 'UK' },
  { label: '马来西亚', value: 'MY' },
];

export default function BrandList() {
  const [brands, setBrands] = useState<BrandItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [country, setCountry] = useState<string | undefined>();

  const fetchBrands = async () => {
    setLoading(true);
    try {
      const res = await getBrands({ page: 1, size: 100, country });
      setBrands(res.data.data.items);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBrands();
  }, [country]);

  return (
    <div>
      <div className="mb-4">
        <Select
          allowClear
          placeholder="按国家筛选"
          style={{ width: 200 }}
          value={country}
          onChange={(v) => setCountry(v)}
          options={COUNTRY_OPTIONS}
        />
      </div>
      {loading ? (
        <Spin size="large" className="block text-center mt-12" />
      ) : (
        <Row gutter={[16, 16]}>
          {brands.map((b) => (
            <Col key={b.id} xs={24} sm={12} md={8} lg={6}>
              <BrandCard brand={b} />
            </Col>
          ))}
        </Row>
      )}
    </div>
  );
}
