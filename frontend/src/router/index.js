import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Login from '@/components/Login/Login'
import Callback from '@/components/Login/Callback'
import Dashboard from '@/components/Dashboard/Dashboard'
import PartsAnalysis from '@/components/Parts/Analysis'
import PartsAnalysisList from '@/components/Parts/AnalysisList'
import PartsAnalysisSummary from '@/components/Parts/AnalysisSummary'
import SpareDetails from '@/components/Parts/SpareDetails'
import DynamicTable from '@/components/Parts/Table'
import Reference from '@/components/Reference/Reference'
import ErrorSummary from '@/components/Parts/ErrorSummary'
import CreateAnalysis from '@/components/Parts/CreateAnalysis'
import ReferenceView from '@/components/Reference/ReferenceView'
import UserRoleManagement from '@/components/ManageRoles/UserRoleManagement'
import ChangePassword from '@/components/ManageRoles/ChangePassword'
import ManageUser from '@/components/ManageRoles/ManageUser'
import SolutionScreen from '@/components/MockUp/SolutionScreen'
import MockUpNew from '@/components/MockUp/MockUpNew'
import TestPlanKnowledgeMap from '@/components/KnowledgeMap/TestPlanKnowledgeMap'
import KnowledgeMap from '@/components/KnowledgeMap/KnowledgeMap'
import FsbKnowledgeMap from '@/components/KnowledgeMap/FsbKnowledgeMap'
import MopKnowledgeMap from '@/components/KnowledgeMap/MopKnowledgeMap'
import ReleaseNotesKnowledgeMap from '@/components/KnowledgeMap/ReleaseNotesKnowledgeMap'
import TechNotesKnowledgeMap from '@/components/KnowledgeMap/TechNotesKnowledgeMap'
Vue.use(Router)

export default new Router({
  mode: 'history',

  routes: [{
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    }, {
      path: '/callback',
      name: 'callback',
      component: Callback
    }, {
      path: '/dashboard',
      name: 'Dashboard',
      component: Dashboard,
      meta: {
        permission: 'Dashboard'
      }
    }, {
      path: '/parts/analysis/create',
      name: 'CreateAnalysis',
      component: CreateAnalysis,
      meta: {
        permission: 'CreateAnalysis'
      }
    }, {
      path: '/parts/analysis/view',
      name: 'PartsAnalysis',
      component: PartsAnalysis,
      meta: {
        permission: 'ViewAnalysis'
      }
    }, {
      path: '/parts/analysis/dashboard',
      name: 'PartsAnalysisList',
      component: PartsAnalysisList,
      meta: {
        permission: 'ViewAnalysis'
      }
    }, {
      path: '/parts/analysis/summary',
      name: 'PartsAnalysisSummary',
      component: PartsAnalysisSummary,
      meta: {
        permission: 'ViewAnalysisDetails'
      }
    },
    {
      path: '/parts/analysis',
      name: 'SpareDetails',
      component: SpareDetails,
      meta: {
        permission: 'ViewAnalysisDetails'
      }
    },
    {
      path: '/table',
      name: 'DynamicTable',
      component: DynamicTable,
      meta: {
        permission: 'Dashboard'
      }
    },
    {
      path: '/reference',
      name: 'Reference',
      component: Reference,
      meta: {
        permission: 'ViewReference'
      }
    },
    {
      path: '/reference/view',
      name: 'ReferenceView',
      component: ReferenceView,
      meta: {
        permission: 'ViewReference'
      }
    },
    {
      path: '/parts/analysis/error',
      name: 'ErrorSummary',
      component: ErrorSummary,
      meta: {
        permission: 'ViewAnalysisDetails'
      }
    },
    {
      path: '/role',
      name: 'UserRoleManagement',
      component: UserRoleManagement,
      meta: {
        permission: 'ManageRole'
      }
    },
    {
      path: '/user',
      name: 'ManageUser',
      component: ManageUser,
      meta: {
        permission: 'ManageUser'
      }
    },
    {
      path: '/password',
      name: 'ChangePassword',
      component: ChangePassword,
      meta: {
        permission: 'Dashboard'
      }
    },
    {
      path: '/mockuptest',
      name: 'SolutionScreen',
      component: SolutionScreen,
      meta: {
        permission: 'none'
      }
    },
    {
      path: '/solution',
      name: 'MockUpNew',
      component: MockUpNew,
      meta: {
        permission: 'Dashboard'
      }
    },
    {
      path: '/knowledge/testplan',
      name: 'KnowledgeMap',
      component: TestPlanKnowledgeMap,
      meta: {
        permission: 'knowledgeMap'
      }
    },
    {
      path: '/knowledge/fsb',
      name: 'FSBKnowledgeMap',
      component: FsbKnowledgeMap,
      meta: {
        permission: 'knowledgeMap'
      }
    },
    {
      path: '/knowledge/releasenotes',
      name: 'ReleaseNotesKnowledgeMap',
      component: ReleaseNotesKnowledgeMap,
      meta: {
        permission: 'knowledgeMap'
      }
    },
    {
      path: '/knowledge/mop',
      name: 'MopKnowledgeMap',
      component: MopKnowledgeMap,
      meta: {
        permission: 'knowledgeMap'
      }
    },
    {
      path: '/knowledge/technotes',
      name: 'TechNotesKnowledgeMap',
      component: TechNotesKnowledgeMap,
      meta: {
        permission: 'knowledgeMap'
      }
    },
    {
      path: '/knowledge',
      name: 'KnowledgeMap',
      component: KnowledgeMap,
      meta: {
        permission: 'knowledgeMap'
      }
    }
  ]

})
