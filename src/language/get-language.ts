import english from './english'
import chineseSimplified from './chinese-simplified'
import { Language } from './index'
import { LanguageEnum } from '../models'

const getLanguage = (languageEnum: LanguageEnum): Language => {
  switch (languageEnum) {
    case 'ChineseSimplified':
      return chineseSimplified
    case 'English':
      return english
    default:
      return english
  }
}

export { getLanguage }
