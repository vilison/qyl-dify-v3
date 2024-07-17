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
import { useAppContext } from '@/context/app-context'
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
  const { currentWorkspace } = useAppContext()
  const [currCategory, setCurrCategory] = useTabSearchParams({
    defaultTab: allCategoriesEn,
    disableSearchParams: pageType !== PageType.EXPLORE,
  })
  const [allList, setAllList] = useState([])
  const [installedApps, setInstalledApps] = useState([])

  const [mobileAllList, setMobileAllList] = useState([])

  const [tagList, setTagList] = useState([])
  const getTagList = async () => {
    const res = await fetchTagList('app')
    setTagList(res)
    res.filter(item => item.name === 'rma').forEach((item) => {
      if (currCategory === '' || currCategory === `${allCategoriesEn}`)
        getApplist(item.id)
    })
  }

  async function getApplist(param: any) {
    let ids = ''
    if (param.length !== 0)
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
    const newList: any[] = []
    if (currCategory === '' || currCategory === `${allCategoriesEn}`) {
      installedApps.forEach((item) => {
        newList.push({ ...item.app, id: item.id })
      })
      return newList
    }
    else {
      installedApps.forEach((item) => {
        for (const v in allList) {
          if (item.app.id === allList[v].id) {
            console.log(allList, 'allList')

            allList[v].id = item.id
            newList.push(allList[v])
          }
        }
      })

      return newList
    }
  }, [installedApps, allList])

  const mobileList = useMemo(() => {
    // setMobileAllList([])
    // 使用 .map 方法而不是直接修改 mobileAllList
    const List = []
    if (isMobile) {
      const fetchLists = tagList.map(item =>
        fetchAppList({ url: 'installed-apps/tags', params: { tag_ids: item.id } }),
      )
      Promise.all(fetchLists).then((results) => {
        const List = results.map((data, index) => ({
          name: tagList[index].name,
          data: data.data,
          tag_id: tagList[index].id,
        }))
        setMobileAllList(List)
        return List
      })
    }
    else {
      if (currCategory !== `${allCategoriesEn}` && currCategory !== '') {
        tagList.filter(item => item.name === currCategory).forEach((item) => {
          setCurrTagId(item.id)
          getApplist(item.id)
        })
      }
    }
  }, [tagList])

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
      isMobile && 'overflow-auto',
    )}>
      {pageType === PageType.EXPLORE && (
        <div className={cn('shrink-0 pt-6', isMobile === true ? 'px-8' : 'px-12')}>
          <div className={`mb-1 ${s.textGradient} text-xl font-semibold`}>{currentWorkspace.name}</div>
          <div className='text-gray-500 text-sm'>&#128075; {t('racio.apps.description')} &#128640; </div>
        </div>
      )
      }
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
      {

        isMobile && (

          <div className='relative flex flex-1 p-6 flex-col bg-sky-50 shrink-0 grow gap-4'>
            {mobileAllList.map((item, index) => (
              <React.Fragment key={index}>
                {item.data.length > 0 && (
                  <>
                    <div className='text-black text-l font-bold'>{item.name === 'rma' ? `${allCategoriesEn}` : item.name}</div>
                    {item.data.map((items, idx) => (
                      <MappCard
                        key={items.id + idx}
                        isExplore={pageType === PageType.EXPLORE}
                        app={items.app}
                        appId={items.id}
                        canCreate={hasEditPermission}
                        onOpen={(id) => {
                          onOpen(id)
                        }}
                      />
                    ))}
                  </>
                )}
              </React.Fragment>
            ))}
          </div>

        )

      }
      {
        !isMobile && (
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
          </div>)
      }

    </div >
  )
}

export default React.memo(Apps)
