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
import MappCard from '@/app/components/racio-office/app-card/m-index'
import { fetchAppList } from '@/service/apps'
import { fetchTagList } from '@/service/tag'
import { useTabSearchParams } from '@/hooks/use-tab-searchparams'
import AppTypeSelector from '@/app/components/app/type-selector'
import Loading from '@/app/components/base/loading'
import { fetchInstalledAppList as doFetchInstalledAppList } from '@/service/explore'
import useBreakpoints, { MediaType } from '@/hooks/use-breakpoints'

type AppsProps = {
  pageType?: PageType
  onSuccess?: () => void
}

export enum PageType {
  EXPLORE = 'office',
  CREATE = 'create',
}

const Apps = ({
  pageType = PageType.EXPLORE,
  onSuccess,
}: AppsProps) => {
  const { t } = useTranslation()
  const { push } = useRouter()
  const { hasEditPermission } = useContext(ExploreContext)
  const allCategoriesEn = t('racio.apps.allCategories', { lng: 'en' })
  const media = useBreakpoints()
  const isMobile = media === MediaType.mobile
  const [currentType, setCurrentType] = useState<string>('')
  const [currTagId, setCurrTagId] = useState('')
  const [currCategory, setCurrCategory] = useTabSearchParams({
    defaultTab: allCategoriesEn,
    disableSearchParams: pageType !== PageType.EXPLORE,
  })
  const [allList, setAllList] = useState([])
  const [installedApps, setInstalledApps] = useState([])
  const [rmaTagId, setRmaTagId] = useState([])
  const [mobileAllList, setMobileAllList] = useState([])
  // var mobileAllList = []
  // const tagList = useTagStore(s => s.tagList)
  // const setTagList = useTagStore(s => s.setTagList)
  const [tagList, setTagList] = useState([])
  const getTagList = async () => {
    const res = await fetchTagList('app')
    setTagList(res)
    res.filter(item => item.name === 'rma').map((item) => {
      setRmaTagId(item.id)
      console.log(currCategory)
      if (currCategory === '' || currCategory === '推荐')
        getApplist(item.id)
    })

    if (isMobile) {
      res.map(async (item) => {
        console.log(item.id, 'item.id')

        fetchAppList({ url: '/apps', params: { tag_ids: item.id } }).then((result) => {
          setMobileAllList(prevList => [...prevList, { name: item.name, data: result.data, id: item.id }])
        }).catch((err) => {

        })
      })
    }
    else {
      if (currCategory != '推荐' && currCategory != '') {
        res.filter(item => item.name === currCategory).map((item) => {
          setCurrTagId(item.id)
          getApplist(item.id)
        })
      }
    }
  }

  async function getApplist(param: any) {
    let ids = ''
    if (param.length != 0)
      ids = param
    else
      ids = currTagId

    const { data: appList, mutate: mutateApps } = await fetchAppList({ url: '/apps', params: { tag_ids: ids } })
    setAllList(appList)
  }

  async function fetchInstalledAppList() {
    const { installed_apps }: any = await doFetchInstalledAppList()
    setInstalledApps(installed_apps)
  }

  useEffect(() => {
    fetchInstalledAppList()
    getTagList()
  }, [])

  const filteredList = useMemo(() => {
    console.log(tagList, currCategory, 'dddtagList', mobileAllList, 'mobileAllList')

    installedApps.map((item) => {
      for (const v in allList) {
        if (item.app.id == allList[v].id)
          allList[v].id = item.id
      }
    })
    return allList
  }, [currCategory, installedApps, allList])

  const [currApp, setCurrApp] = React.useState<App | null>(null)
  const [isShowCreateModal, setIsShowCreateModal] = React.useState(false)

  const onOpen = (id: string) => {
    const url = `/office/installed/${id}`
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
        {!isMobile && (
          <Category
            list={tagList}
            value={currCategory}
            onChange={setCurrCategory}
            allCategoriesEn={allCategoriesEn}
          />)}
      </div>
      {!isMobile && (
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
        </div>)}
      {isMobile && (
        <div className='relative flex flex-1 p-6 flex-col overflow-auto bg-sky-50 shrink-0 grow gap-4'>
          {mobileAllList.map((app, index) => (
            <React.Fragment key={app.id + index}>
              {app.data.length > 1 && (
                <>
                  <div className='text-black text-l font-bold'>{app.name === 'rma' ? '推荐' : app.name}</div>
                  {app.data.map(item => (
                    <MappCard
                      key={item.id}
                      isExplore={pageType === PageType.EXPLORE}
                      app={item}
                      canCreate={hasEditPermission}
                      onOpen={() => {
                        onOpen(item.id)
                      }}
                    />
                  ))}
                </>
              )}
            </React.Fragment>
          ))}
        </div>
      )}
    </div>
  )
}

export default React.memo(Apps)
