'use client'
import type { FC } from 'react'
import React, { useEffect } from 'react'
import { useTranslation } from 'react-i18next'

type IAppUnavailableProps = {
  code?: number
  isUnknwonReason?: boolean
  unknownReason?: string
}

const AppUnavailable: FC<IAppUnavailableProps> = ({
  code = 404,
  isUnknwonReason,
  unknownReason,
}) => {
  useEffect(() => {
    if (code === 404) {
      let appErrorReplaceUrl404 = ''

      if (process.env.NEXT_PUBLIC_APP_ERROR_REPLACE_URL_404) {
        appErrorReplaceUrl404 = process.env.NEXT_PUBLIC_APP_ERROR_REPLACE_URL_404
      }
      else if (
        globalThis.document?.body?.getAttribute('data-public-app-error-replace-url-404')
      ) {
        // Not bulild can not get env from process.env.NEXT_PUBLIC_ in browser https://nextjs.org/docs/basic-features/environment-variables#exposing-environment-variables-to-the-browser
        appErrorReplaceUrl404 = globalThis.document?.body?.getAttribute('data-public-app-error-replace-url-404') as string
      }
      else {
        appErrorReplaceUrl404 = 'https://at.racio.chat/chat/XwzsksyMCKupYvIr' // default support url
      }
      window.location.replace(appErrorReplaceUrl404)
    }
  }, [code, isUnknwonReason, unknownReason])

  const { t } = useTranslation()

  return (
    <div className='flex items-center justify-center w-screen h-screen'>
      <h1 className='mr-5 h-[50px] leading-[50px] pr-5 text-[24px] font-medium'
        style={{
          borderRight: '1px solid rgba(0,0,0,.3)',
        }}>{code}</h1>
      <div className='text-sm'>{unknownReason || (isUnknwonReason ? t('share.common.appUnkonwError') : t('share.common.appUnavailable'))}</div>
    </div>
  )
}

export default React.memo(AppUnavailable)
