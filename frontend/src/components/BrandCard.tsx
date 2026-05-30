import { useNavigate } from 'react-router-dom';
import { Card } from 'antd';
import type { BrandItem } from '../api/brand';

export default function BrandCard({ brand }: { brand: BrandItem }) {
  const navigate = useNavigate();
  return (
    <Card
      hoverable
      onClick={() => navigate(`/brands/${brand.id}`)}
      cover={
        brand.logo_url ? (
          <img alt={brand.name} src={brand.logo_url} className="h-40 object-cover" />
        ) : (
          <div className="h-40 bg-gray-100 flex items-center justify-center text-gray-400">暂无图片</div>
        )
      }
    >
      <Card.Meta
        title={brand.name}
        description={`${brand.country} | ${brand.juice_count} 款烟油`}
      />
    </Card>
  );
}
