import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Spin, Descriptions, Rate, Tag, Image, Empty } from 'antd';
import { getJuice } from '../api/juice';
import type { JuiceItem } from '../api/juice';

export default function JuiceDetail() {
  const { id } = useParams<{ id: string }>();
  const [juice, setJuice] = useState<JuiceItem | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    getJuice(Number(id)).then((res) => setJuice(res.data.data)).finally(() => setLoading(false));
  }, [id]);

  if (loading) return <Spin size="large" className="block text-center mt-12" />;
  if (!juice) return <Empty description="烟油不存在" />;

  return (
    <div>
      <div className="flex flex-col md:flex-row gap-6 mb-8">
        <div className="w-full md:w-64">
          {juice.image_urls.length > 0
            ? <Image src={juice.image_urls[0]} alt={juice.name} className="rounded-lg" />
            : <div className="w-64 h-64 bg-gray-100 flex items-center justify-center text-gray-400 rounded-lg">暂无图片</div>}
        </div>
        <div className="flex-1">
          <h1 className="text-2xl font-bold mb-2">{juice.name}</h1>
          <div className="text-gray-500 mb-2">{juice.brand_name}</div>
          <div className="flex items-center gap-2 mb-4">
            <Rate disabled value={juice.avg_rating / 2} allowHalf />
            <span>({juice.review_count} 条评论)</span>
          </div>
          <div className="flex gap-1 flex-wrap mb-4">
            {juice.tags.map((t) => (<Tag key={t.id}>{t.name}</Tag>))}
          </div>
        </div>
      </div>
      <Descriptions bordered column={{ xs: 1, sm: 2 }} title="详细信息">
        <Descriptions.Item label="味型">{juice.flavor_profile || '-'}</Descriptions.Item>
        <Descriptions.Item label="尼古丁">{juice.nicotine_range || '-'}</Descriptions.Item>
        <Descriptions.Item label="VG/PG">{juice.vg_pg_ratio || '-'}</Descriptions.Item>
        <Descriptions.Item label="容量">{juice.volume || '-'}</Descriptions.Item>
        <Descriptions.Item label="参考价格">{juice.price_range || '-'}</Descriptions.Item>
      </Descriptions>
      {juice.description && <p className="mt-4 text-gray-600">{juice.description}</p>}
      {/* 评论区留空，Task 14 补充 */}
    </div>
  );
}
