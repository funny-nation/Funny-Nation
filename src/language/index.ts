import englishLanguage from './english-language'
import chineseSimpleLanguage from './chinese-simple-language'
import { Language } from './Language'

const getLanguage = (language: string = ''): Language => {
  switch (language) {
    case 'ChineseSimple':
      return chineseSimpleLanguage
    case 'English':
      return englishLanguage
    default:
      return englishLanguage
  }
}

export default getLanguage
