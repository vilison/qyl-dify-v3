const translation = {
  pageTitle: {
    line1: '提示词',
    line2: '编排',
  },
  orchestrate: '编排',
  promptMode: {
    simple: '切换到专家模式以编辑完整的提示词',
    advanced: '专家模式',
    switchBack: '返回简易模式',
    advancedWarning: {
      title: '您已切换到专家模式，一旦修改提示词，将无法返回简易模式。',
      description: '在专家模式下，您可以编辑完整的提示词。',
      learnMore: '了解更多',
      ok: '确定',
    },
    operation: {
      addMessage: '添加消息',
    },
    contextMissing: '上下文内容块缺失，提示词的有效性可能不好。',
  },
  operation: {
    applyConfig: '发布',
    resetConfig: '重置',
    debugConfig: '调试',
    addFeature: '添加功能',
    automatic: '自动编排',
    stopResponding: '停止响应',
    agree: '赞同',
    disagree: '反对',
    cancelAgree: '取消赞同',
    cancelDisagree: '取消反对',
    userAction: '用户表示',
  },
  notSetAPIKey: {
    title: 'LLM 提供者的密钥未设置',
    trailFinished: '试用已结束',
    description: '在调试之前需要设置 LLM 提供者的密钥。',
    settingBtn: '去设置',
  },
  trailUseGPT4Info: {
    title: '当前不支持使用 gpt-4',
    description: '使用 gpt-4，请设置 API Key',
  },
  feature: {
    groupChat: {
      title: '聊天增强',
      description: '为聊天型应用添加预对话设置，可以提升用户体验。',
    },
    groupExperience: {
      title: '体验增强',
    },
    conversationOpener: {
      title: '对话开场白',
      description: '在对话型应用中，让 AI 主动说第一段话可以拉近与用户间的距离。',
    },
    suggestedQuestionsAfterAnswer: {
      title: '下一步问题建议',
      description: '设置下一步问题建议可以让用户更好的对话。',
      resDes: '回答结束后系统会给出 3 个建议',
      tryToAsk: '试着问问',
    },
    moreLikeThis: {
      title: '更多类似的',
      description: '一次生成多条文本，可在此基础上编辑并继续生成',
      generateNumTip: '每次生成数',
      tip: '使用此功能将会额外消耗 tokens',
    },
    speechToText: {
      title: '语音转文字',
      description: '启用后，您可以使用语音输入。',
      resDes: '语音输入已启用',
    },
    textToSpeech: {
      title: '文字转语音',
      description: '启用后，文本可以转换成语音。',
      resDes: '文本转音频已启用',
    },
    citation: {
      title: '引用和归属',
      description: '启用后，显示源文档和生成内容的归属部分。',
      resDes: '引用和归属已启用',
    },
    annotation: {
      title: '标注回复',
      description: '启用后，将标注用户的回复，以便在用户重复提问时快速响应。',
      resDes: '标注回复已启用',
      scoreThreshold: {
        title: '分数阈值',
        description: '用于设置标注回复的匹配相似度阈值。',
        easyMatch: '容易匹配',
        accurateMatch: '精准匹配',
      },
      matchVariable: {
        title: '匹配变量',
        choosePlaceholder: '请选择变量',
      },
      cacheManagement: '标注管理',
      cached: '已标注',
      remove: '移除',
      removeConfirm: '删除这个标注？',
      add: '添加标注',
      edit: '编辑标注',
    },
    dataSet: {
      title: '上下文',
      noData: '您可以导入知识库作为上下文',
      words: '词',
      textBlocks: '文本块',
      selectTitle: '选择引用知识库',
      selected: '个知识库被选中',
      noDataSet: '未找到知识库',
      toCreate: '去创建',
      notSupportSelectMulti: '目前只支持引用一个知识库',
      queryVariable: {
        title: '查询变量',
        tip: '该变量将用作上下文检索的查询输入，获取与该变量的输入相关的上下文信息。',
        choosePlaceholder: '请选择变量',
        noVar: '没有变量',
        noVarTip: '请创建变量',
        unableToQueryDataSet: '无法查询知识库',
        unableToQueryDataSetTip: '无法成功查询知识库，请在上下文部分选择一个上下文查询变量。',
        ok: '好的',
        contextVarNotEmpty: '上下文查询变量不能为空',
        deleteContextVarTitle: '删除变量“{{varName}}”？',
        deleteContextVarTip: '该变量已被设置为上下文查询变量，删除该变量将影响知识库的正常使用。 如果您仍需要删除它，请在上下文部分中重新选择它。',
      },
    },
    tools: {
      title: '工具',
      tips: '工具提供了一个标准的 API 调用方式，将用户输入或变量作为 API 的请求参数，用于查询外部数据作为上下文。',
      toolsInUse: '{{count}} 工具使用中',
      modal: {
        title: '工具',
        toolType: {
          title: '工具类型',
          placeholder: '请选择工具类型',
        },
        name: {
          title: '名称',
          placeholder: '请填写名称',
        },
        variableName: {
          title: '变量名称',
          placeholder: '请填写变量名称',
        },
      },
    },
    conversationHistory: {
      title: '对话历史',
      description: '设置对话角色的前缀名称',
      tip: '对话历史未启用，请在上面的提示中添加<histories>。',
      learnMore: '了解更多',
      editModal: {
        title: '编辑对话角色名称',
        userPrefix: '用户前缀',
        assistantPrefix: '助手前缀',
      },
    },
    toolbox: {
      title: '工具箱',
    },
    moderation: {
      title: '内容审查',
      description: '您可以调用审查 API 或者维护敏感词库来使模型更安全地输出。',
      allEnabled: '审查输入/审查输出 内容已启用',
      inputEnabled: '审查输入内容已启用',
      outputEnabled: '审查输出内容已启用',
      modal: {
        title: '内容审查设置',
        provider: {
          title: '类别',
          openai: 'OpenAI Moderation',
          openaiTip: {
            prefix: 'OpenAI Moderation 需要在',
            suffix: '中配置 OpenAI API 密钥。',
          },
          keywords: '关键词',
        },
        keywords: {
          tip: '每行一个，用换行符分隔。每行最多 100 个字符。',
          placeholder: '每行一个，用换行符分隔',
          line: '行',
        },
        content: {
          input: '审查输入内容',
          output: '审查输出内容',
          preset: '预设回复',
          placeholder: '这里预设回复内容',
          condition: '审查输入内容和审查输出内容至少启用一项',
          fromApi: '预设回复通过 API 返回',
          errorMessage: '预设回复不能为空',
          supportMarkdown: '支持 Markdown',
        },
        openaiNotConfig: {
          before: 'OpenAI 内容审查需要在',
          after: '中配置 OpenAI API 密钥。',
        },
      },
    },
  },
  automatic: {
    title: '自动编排',
    description: '描述您的场景，Racio 将为您编排一个应用。',
    intendedAudience: '目标用户是谁？',
    intendedAudiencePlaceHolder: '例如：学生',
    solveProblem: '希望 AI 为他们解决什么问题？',
    solveProblemPlaceHolder: '例如：评估学业水平',
    generate: '生成',
    audiencesRequired: '目标用户必填',
    problemRequired: '解决问题必填',
    resTitle: '我们为您编排了以下应用程序',
    apply: '应用',
    noData: '在左侧描述您的用例，编排预览将在此处显示。',
    loading: '为您编排应用程序中…',
    overwriteTitle: '覆盖现有配置？',
    overwriteMessage: '应用此编排将覆盖现有配置。',
  },
  resetConfig: {
    title: '确认重置？',
    message: '重置将丢失当前页面所有修改，恢复至上次发布时的配置',
  },
  errorMessage: {
    nameOfKeyRequired: '变量 {{key}} 对应的名称必填',
    valueOfVarRequired: '{{key}}必填',
    queryRequired: '主要文本必填',
    waitForResponse: '请等待上条信息响应完成',
    waitForBatchResponse: '请等待批量任务完成',
    notSelectModel: '请选择模型',
    waitForImgUpload: '请等待图片上传完成',
  },
  chatSubTitle: '提示词',
  completionSubTitle: '前缀提示词',
  promptTip:
    '提示词用于对 AI 的回复做出一系列指令和约束。可插入表单变量，例如 {{input}}。这段提示词不会被最终用户所看到。',
  formattingChangedTitle: '编排已改变',
  formattingChangedText: '修改编排将重置调试区域，确定吗？',
  variableTitle: '变量',
  notSetVar: '变量能使用户输入表单引入提示词或开场白，你可以试试在提示词中输入 {{input}}',
  variableTip:
    '变量将以表单形式让用户在对话前填写，用户填写的表单内容将自动替换提示词中的变量。',
  autoAddVar: '提示词中引用了未定义的变量，是否自动添加到用户输入表单中？',
  variableTable: {
    key: '变量 Key',
    name: '字段名称',
    optional: '可选',
    type: '类型',
    action: '操作',
    typeString: '文本',
    typeSelect: '下拉选项',
  },
  varKeyError: {
    canNoBeEmpty: '变量不能为空',
    tooLong: '变量: {{key}} 长度太长。不能超过 30 个字符',
    notValid: '变量: {{key}} 非法。只能包含英文字符，数字和下划线',
    notStartWithNumber: '变量: {{key}} 不能以数字开头',
    keyAlreadyExists: '变量:{{key}} 已存在',
  },
  otherError: {
    promptNoBeEmpty: '提示词不能为空',
    historyNoBeEmpty: '提示词中必须设置对话历史',
    queryNoBeEmpty: '提示词中必须设置查询内容',
  },
  variableConig: {
    'addModalTitle': '添加变量',
    'editModalTitle': '编辑变量',
    'description': '设置变量 {{varName}}',
    'fieldType': '字段类型',
    'string': '文本',
    'text-input': '文本',
    'paragraph': '段落',
    'select': '下拉选项',
    'number': '数字',
    'notSet': '未设置，在 Prompt 中输入 {{input}} 试试',
    'stringTitle': '文本框设置',
    'maxLength': '最大长度',
    'options': '选项',
    'addOption': '添加选项',
    'apiBasedVar': '基于 API 的变量',
    'varName': '变量名称',
    'inputPlaceholder': '请输入',
    'labelName': '显示名称',
    'required': '必填',
    'errorMsg': {
      varNameRequired: '变量名称必填',
      labelNameRequired: '显示名称必填',
      varNameCanBeRepeat: '变量名称不能重复',
      atLeastOneOption: '至少需要一个选项',
      optionRepeat: '选项不能重复',
    },
  },
  vision: {
    name: '视觉',
    description: '开启视觉功能将允许模型输入图片，并根据图像内容的理解回答用户问题',
    settings: '设置',
    visionSettings: {
      title: '视觉设置',
      resolution: '分辨率',
      resolutionTooltip: `低分辨率模式将使模型接收图像的低分辨率版本，尺寸为512 x 512，并使用65 Tokens 来表示图像。这样可以使API更快地返回响应，并在不需要高细节的用例中消耗更少的输入。
      \n
      高分辨率模式将首先允许模型查看低分辨率图像，然后根据输入图像的大小创建512像素的详细裁剪图像。每个详细裁剪图像使用两倍的预算总共为129 Tokens。`,
      high: '高',
      low: '低',
      uploadMethod: '上传方式',
      both: '两者',
      localUpload: '本地上传',
      url: 'URL',
      uploadLimit: '上传数量限制',
    },
  },
  voice: {
    name: '音色',
    defaultDisplay: '缺省音色',
    description: '文本转语音音色设置',
    settings: '设置',
    voiceSettings: {
      title: '音色设置',
      language: '语言',
      resolutionTooltip: '文本转语音音色支持语言。',
      voice: '音色',
    },
  },
  openingStatement: {
    title: '对话开场白',
    add: '添加开场白',
    writeOpener: '编写开场白',
    placeholder: '在这里写下你的开场白，你可以使用变量，尝试输入 {{variable}}。',
    openingQuestion: '开场问题',
    noDataPlaceHolder:
      '在对话型应用中，让 AI 主动说第一段话可以拉近与用户间的距离。',
    varTip: '你可以使用变量， 试试输入 {{variable}}',
    tooShort: '对话前提示词至少 20 字才能生成开场白',
    notIncludeKey: '前缀提示词中不包含变量 {{key}}。请在前缀提示词中添加该变量',
  },
  modelConfig: {
    model: '语言模型',
    setTone: '模型设置',
    title: '模型及参数',
    modeType: {
      chat: '对话型',
      completion: '补全型',
    },
  },
  inputs: {
    title: '调试与预览',
    noPrompt: '尝试在对话前提示框中编写一些提示词',
    userInputField: '用户输入',
    noVar: '填入变量的值，每次启动新会话时该变量将自动替换提示词中的变量。',
    chatVarTip: '填入变量的值，该值将在每次开启一个新会话时自动替换到提示词中',
    completionVarTip: '填入变量的值，该值将在每次提交问题时自动替换到提示词中',
    previewTitle: '提示词预览',
    queryTitle: '查询内容',
    queryPlaceholder: '请输入文本内容',
    run: '运行',
  },
  result: '结果',
  datasetConfig: {
    settingTitle: '召回设置',
    knowledgeTip: '点击 “+” 按钮添加知识库',
    retrieveOneWay: {
      title: 'N选1召回',
      description: '根据用户意图和知识库描述，由 Agent 自主判断选择最匹配的单个知识库来查询相关文本，适合知识库区分度大且知识库数量偏少的应用。',
    },
    retrieveMultiWay: {
      title: '多路召回',
      description: '根据用户意图同时匹配所有知识库，从多路知识库查询相关文本片段，经过重排序步骤，从多路查询结果中选择匹配用户问题的最佳结果，需配置 Rerank 模型 API。',
    },
    rerankModelRequired: '请选择 Rerank 模型',
    params: '参数设置',
    top_k: 'Top K',
    top_kTip: '用于筛选与用户问题相似度最高的文本片段。系统同时会根据选用模型上下文窗口大小动态调整分段数量。',
    score_threshold: 'Score 阈值',
    score_thresholdTip: '用于设置文本片段筛选的相似度阈值。',
    retrieveChangeTip: '修改索引模式和检索模式可能会影响与该知识库关联的应用程序。',
  },
  debugAsSingleModel: '单一模型进行调试',
  debugAsMultipleModel: '多个模型进行调试',
  duplicateModel: '复制模型',
  publishAs: '发布为',
  assistantType: {
    name: '助手类型',
    chatAssistant: {
      name: '基础助手',
      description: '基于 LLM 构建一个聊天型助手',
    },
    agentAssistant: {
      name: '智能助手',
      description: '构建一个智能助手，他可以自主选择工具完成你设置的任务',
    },
  },
  agent: {
    agentMode: 'Agent Mode',
    agentModeDes: '设置代理的推理模式类型',
    agentModeType: {
      ReACT: 'ReAct',
      functionCall: 'Function Calling',
    },
    setting: {
      name: 'Agent 设置',
      description: '智能助手设置允许设置代理模式和内置提示等高级功能，仅在代理类型中可用。',
      maximumIterations: {
        name: '最大迭代次数',
        description: '限制代理型助手执行迭代的次数',
      },
    },
    buildInPrompt: '内置提示词',
    firstPrompt: '第一次提示词',
    nextIteration: '下一次迭代',
    promptPlaceholder: '在这里写下您的提示词',
    tools: {
      name: '工具',
      description: '使用工具可以扩展代理的能力，比如搜索互联网或科学计算',
      enabled: '启用',
    },
  },
}

export default translation
