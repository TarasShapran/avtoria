import {useForm} from "react-hook-form";
import {carService} from "../../services/carService";

const CarForm = () => {
    const {register, handleSubmit, reset} = useForm();


    const save = async (car) => {
        await carService.create(car)
        reset()
    }
    return (
        <form onSubmit={handleSubmit(save)}>
            <input type="text" placeholder={'model'} {...register('model')}/>
            <input type="text" placeholder={'body_type'} {...register('body_type')}/>
            <input type="text" placeholder={'price'} {...register('price')}/>
            <input type="text" placeholder={'year'} {...register('year')}/>
            <button>save</button>
        </form>
    );
};

export {CarForm};