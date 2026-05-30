import { useNavigate } from 'react-router-dom';
import { Card, Rate, Tag } from 'antd';
import type { JuiceItem } from '../api/juice';

export default function JuiceCard({ juice }: { juice: JuiceItem }) {
  const navigate = useNavigate();
  return (
    <Card hoverable onClick={() => navigate(`/juices/${juice.id}`)} cover={
      juice.image_urls.length > 0
        ? <img alt={juice.name} src={juice.image_urls[0]} className="h-40 object-cover" />
        : <div className="h-40 bg-gray-100 flex items-center justify-center text-gray-400">暂无图片</div>
    }>
      <Card.Meta
        title={<div className="flex justify-between items-center"><span>{juice.name}</span><span className="text-sm text-gray-400">{juice.price_range}</span></div>}
        description={
          <div>
            <div className="text-gray-500 text-sm mb-1">{juice.brand_name}</div>
            <div className="flex items-center gap-1 mb-1">
              <Rate disabled value={juice.avg_rating / 2} allowHalf style={{ fontSize: 14 }} />
              <span className="text-xs text-gray-400">({juice.review_count})</span>
            </div>
            <div className="flex gap-1 flex-wrap">
              {juice.tags.map((t) => (<Tag key={t.id}>{t.name}</Tag>))}
            </div>
          </div>
        }
      />
    </Card>
  );
}
