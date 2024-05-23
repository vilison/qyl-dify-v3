import type { FC } from 'react'
import React from 'react'
import RacioOffice from '@/app/components/racio-office'
export type IAppDetail = {
  children: React.ReactNode
}

const AppDetail: FC<IAppDetail> = ({ children }) => {
  return (
    <RacioOffice>
      {children}
    </RacioOffice>
  )
}

export default React.memo(AppDetail)
