ALTER TABLE public.vector_layer ADD COLUMN versioned boolean;
UPDATE public.vector_layer SET versioned = FALSE;
