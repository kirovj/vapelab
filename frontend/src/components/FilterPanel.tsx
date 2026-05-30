import { Select, Space } from 'antd';

const FLAVOR_OPTIONS = [
  { label: '全部味型', value: '' },
  { label: '水果', value: '水果' },
  { label: '甜点', value: '甜点' },
  { label: '烟草', value: '烟草' },
  { label: '薄荷', value: '薄荷' },
  { label: '饮品', value: '饮品' },
];

const SORT_OPTIONS = [
  { label: '最新', value: 'newest' },
  { label: '评分最高', value: 'rating_desc' },
  { label: '评分最低', value: 'rating_asc' },
];

interface FilterPanelProps {
  flavor: string | undefined;
  onFlavorChange: (v: string | undefined) => void;
  sort: string;
  onSortChange: (v: string) => void;
}

/** 搜索页面的筛选面板：味型筛选 + 排序 */
export default function FilterPanel({ flavor, onFlavorChange, sort, onSortChange }: FilterPanelProps) {
  return (
    <Space className="mb-4">
      <Select
        allowClear
        placeholder="味型筛选"
        style={{ width: 150 }}
        value={flavor}
        onChange={onFlavorChange}
        options={FLAVOR_OPTIONS}
      />
      <Select
        style={{ width: 150 }}
        value={sort}
        onChange={onSortChange}
        options={SORT_OPTIONS}
      />
    </Space>
  );
}
