'use client'

import React, { useEffect, useMemo, useState } from 'react'
import cn from 'classnames'
import { useRouter } from 'next/navigation'
import { useTranslation } from 'react-i18next'
import { useContext } from 'use-context-selector'
import s from './style.module.css'
import ExploreContext from '@/context/explore-context'
import type { App } from '@/models/explore'
import Category from '@/app/components/racio-office/category'
import AppCard from '@/app/components/racio-office/app-card'
import { fetchAppList } from '@/service/apps'
import { fetchTagList } from '@/service/tag'
import { useTabSearchParams } from '@/hooks/use-tab-searchparams'
import AppTypeSelector from '@/app/components/app/type-selector'
import Loading from '@/app/components/base/loading'
import { useAppContext } from '@/context/app-context'
import { useStore as useTagStore } from '@/app/components/base/tag-management/store'
import { fetchInstalledAppList as doFetchInstalledAppList } from '@/service/explore'
type AppsProps = {
  pageType?: PageType
  onSuccess?: () => void
}

export enum PageType {
  EXPLORE = 'explore',
  CREATE = 'create',
}

const Apps = ({
  pageType = PageType.EXPLORE,
  onSuccess,
}: AppsProps) => {
  const { t } = useTranslation()
  const { isCurrentWorkspaceManager } = useAppContext()
  const { push } = useRouter()
  const { hasEditPermission } = useContext(ExploreContext)
  const allCategoriesEn = t('racio.apps.allCategories', { lng: 'en' })

  const [currentType, setCurrentType] = useState<string>('')
  const [currCategory, setCurrCategory] = useTabSearchParams({
    defaultTab: allCategoriesEn,
    disableSearchParams: pageType !== PageType.EXPLORE,
  })
  const [allList, setAllList] = useState([])
  const [installedApps, setInstalledApps] = useState([])

  let tagNameList: string | string[] = []
  const type = 'app'
  const tagList = useTagStore(s => s.tagList)
  const setTagList = useTagStore(s => s.setTagList)
  const getTagList = async (type: 'knowledge' | 'app') => {
    const res = await fetchTagList(type)
    setTagList(res)
    tagNameList = tagList.map(item => item.name)
    getApplist()
    fetchInstalledAppList()
  }

  const getKey = (
    pageIndex: number,
    previousPageData: AppListResponse,
    activeTab: string,
    tags: string[],
    keywords: string,
  ) => {
    if (!pageIndex || previousPageData.has_more) {
      const params: any = { url: 'apps', params: { page: pageIndex + 1, limit: 30, name: keywords } }

      if (activeTab !== 'all')
        params.params.mode = activeTab
      else
        delete params.params.mode

      if (tags.length)
        params.params.tag_ids = tags

      return params
    }
    return null
  }

  async function getApplist() {
    const { data: appList, mutate: mutateApps } = await fetchAppList({ url: '/apps', params: getKey })
    setAllList(appList)
  }

  async function fetchInstalledAppList() {
    const { installed_apps }: any = await doFetchInstalledAppList()
    setInstalledApps(installed_apps)
  }

  useEffect(() => {
    getTagList(type)
  }, [type])

  const filteredList = useMemo(() => {
    installedApps.map((item) => {
      for (const v in allList) {
        if (item.app.id == allList[v].id)
          allList[v].id = item.id
      }
    })
    return allList
  }, [currentType, currCategory, allCategoriesEn, allList, installedApps])

  const [currApp, setCurrApp] = React.useState<App | null>(null)
  const [isShowCreateModal, setIsShowCreateModal] = React.useState(false)

  const onOpen = (id: string) => {
    const url = `/explore/installed/${id}`
    push(url)
  }

  if (!allList) {
    return (
      <div className="flex h-full items-center">
        <Loading type="area" />
      </div>
    )
  }

  return (
    <div className={cn(
      'flex flex-col',
      pageType === PageType.EXPLORE ? 'h-full border-l border-gray-200' : 'h-[calc(100%-56px)]',
    )}>
      {pageType === PageType.EXPLORE && (
        <div className='shrink-0 pt-6 px-12'>
          <div className={`mb-1 ${s.textGradient} text-xl font-semibold`}>{t('racio.apps.title')}</div>
          <div className='text-gray-500 text-sm'>{t('racio.apps.description')}</div>
        </div>
      )}
      <div className={cn(
        'flex items-center mt-6',
        pageType === PageType.EXPLORE ? 'px-12' : 'px-8',
      )}>
        {pageType !== PageType.EXPLORE && (
          <>
            <AppTypeSelector value={currentType} onChange={setCurrentType} />
            <div className='mx-2 w-[1px] h-3.5 bg-gray-200' />
          </>
        )}
        <Category
          list={tagList}
          value={currCategory}
          onChange={setCurrCategory}
          allCategoriesEn={allCategoriesEn}
        />
      </div>
      <div className={cn(
        'relative flex flex-1 pb-6 flex-col overflow-auto bg-gray-100 shrink-0 grow',
        pageType === PageType.EXPLORE ? 'mt-6' : 'mt-0 pt-2',
      )}>
        <nav
          className={cn(
            s.appList,
            'grid content-start shrink-0',
            pageType === PageType.EXPLORE ? 'gap-4 px-6 sm:px-12' : 'gap-3 px-8  sm:!grid-cols-2 md:!grid-cols-3 lg:!grid-cols-4',
          )}>
          {filteredList.map(app => (
            <AppCard
              key={app.id}
              isExplore={pageType === PageType.EXPLORE}
              app={app}
              canCreate={hasEditPermission}
              onOpen={(id) => {
                onOpen(id)
              }}
            />
          ))}
        </nav>
      </div>
    </div>
  )
}

export default React.memo(Apps)
