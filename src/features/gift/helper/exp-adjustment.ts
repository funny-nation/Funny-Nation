
type ExpAdjustment = {
  senderExp: number,
  receiverExp: number
}

const expAdjustment = (price: number): ExpAdjustment => {
  return {
    senderExp: Math.floor(price * 0.2),
    receiverExp: Math.floor(price * 0.2)
  }
}

export { expAdjustment }
