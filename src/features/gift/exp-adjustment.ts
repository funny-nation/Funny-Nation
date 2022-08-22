
type ExpAdjustment = {
  senderExp: number,
  receiverExp: number
}

const expAdjustment = (price: number): ExpAdjustment => {
  return {
    senderExp: price * 0.2,
    receiverExp: price * 0.2
  }
}

export { expAdjustment }
