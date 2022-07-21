import englishLanguage from './english-language'
import chineseSimpleLanguage from './chinese-simple-language'
import { Language } from './Language'
import LanguageEnum from '../models/LanguageEnum'

const getLanguage = (languageEnum: LanguageEnum): Language => {
  switch (languageEnum) {
    case LanguageEnum.ChineseSimple:
      return chineseSimpleLanguage
    case LanguageEnum.English:
      return englishLanguage
    default:
      return englishLanguage
  }
}

export default getLanguage
