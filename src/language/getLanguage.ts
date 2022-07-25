import english from './english'
import chineseSimple from './chinese-simple'
import { Language } from './index'
import { LanguageEnum } from '../models/enum/LanguageEnum'

const getLanguage = (languageEnum: LanguageEnum): Language => {
  switch (languageEnum) {
    case 'ChineseSimple':
      return chineseSimple
    case 'English':
      return english
    default:
      return english
  }
}

export default getLanguage
