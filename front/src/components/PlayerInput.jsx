function PlayerInput({ value, onChange, index }) {
  return (
    <input
      type="text"
      value={value}
      onChange={e => onChange(index, e.target.value)}
      placeholder={`Joueur ${index + 1}`}
      className="input-field"
    />
  );
}

export default PlayerInput;
