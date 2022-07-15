import sequelize from '../sequelize'
import { DataTypes, Model } from 'sequelize'

class User extends Model {

}

User.init({
  id: {
    type: DataTypes.STRING,
    primaryKey: true
  },
  balance: {
    type: DataTypes.INTEGER
  },
  timeBefore: {
    type: DataTypes.TIME
  },
  experiece: {
    type: DataTypes.INTEGER
  }
}, { sequelize })

export default User
