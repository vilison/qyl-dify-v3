'use client'
import React from 'react'
import type { FC } from 'react'
import { useTranslation } from 'react-i18next'
import cn from 'classnames'
import exploreI18n from '@/i18n/en-US/explore'
import type { AppCategory } from '@/models/explore'
import { ThumbsUp } from '@/app/components/base/icons/src/vender/line/alertsAndFeedback'
const categoryI18n = exploreI18n.category

export type ICategoryProps = {
  className?: string
  list: string[]
  type: 'knowledge' | 'app'
  value: string
  onChange: (value: AppCategory | string) => void
  /**
   * default value for searchparam 'category' in en
   */
  allCategoriesEn: string
}

const Category: FC<ICategoryProps> = ({
  className,
  list,
  value,
  onChange,
  allCategoriesEn,
}) => {
  const { t } = useTranslation()
  const tagNameList = list.map(item => item.name)
  const isAllCategories = !tagNameList.includes(value)

  const itemClassName = (isSelected: boolean) => cn(
    'flex items-center px-3 py-[7px] h-[32px] rounded-lg border-[0.5px] border-transparent text-gray-700 font-medium leading-[18px] cursor-pointer hover:bg-gray-200',
    isSelected && 'bg-white border-gray-200 shadow-xs text-primary-600 hover:bg-white',
  )

  return (
    <div className={cn(className, 'flex space-x-1 text-[13px] flex-wrap')}>
      <div
        className={itemClassName(isAllCategories)}
        onClick={() => onChange(allCategoriesEn)}
      >
        <ThumbsUp className='mr-1 w-3.5 h-3.5' />
        {t('explore.apps.allCategories')}
      </div>

      {list.map((tag) => {
        // 只有当 tag.name 不等于 "rma" 时才渲染该标签
        if (tag.name !== 'rma') {
          return (
            <div
              key={tag.id}
              className={itemClassName(tag.name === value)}
              onClick={() => onChange(tag.name)}
            >
              {tag.name}
            </div>
          )
        }
        // 如果 tag.name 等于 "rma"，则不返回任何内容，即不显示该标签
        return null
      })}
    </div>
  )
}

export default React.memo(Category)
